import base64, re
from email.mime.text import MIMEText
from email.utils import formatdate, make_msgid
from gmail_reader import get_service, list_unread_messages
from templates import TEMPLATES, BLOCKLIST_SENDERS
from classifier import classify_email  # your classifier from Step 4

def _extract_name(from_header: str) -> str:
    # "Name <email@x.com>" -> "Name"
    m = re.match(r'("?)([^"<]+)\1\s*<', from_header)
    return (m.group(2).strip() if m else from_header.split("@")[0]).strip()

def _should_skip(from_header: str) -> bool:
    low = from_header.lower()
    return any(tok in low for tok in BLOCKLIST_SENDERS)

def build_reply_message(to_addr: str, subject: str, body_text: str, in_reply_to: str = "", references: str = "") -> dict:
    msg = MIMEText(body_text, _charset="utf-8")
    msg["To"] = to_addr
    msg["Subject"] = f"Re: {subject}"
    msg["Date"] = formatdate(localtime=True)
    msg["Message-ID"] = make_msgid()
    if in_reply_to:
        msg["In-Reply-To"] = in_reply_to
    if references:
        msg["References"] = f"{references} {in_reply_to}".strip()
    # reduce auto-reply loops
    msg["Auto-Submitted"] = "auto-replied"
    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode("utf-8")
    return {"raw": raw}

def get_or_create_label(service, name="AUTO_REPLIED"):
    # Find label
    labels = service.users().labels().list(userId="me").execute().get("labels", [])
    for lb in labels:
        if lb["name"] == name:
            return lb["id"]
    # Create if missing
    new_lb = service.users().labels().create(userId="me", body={
        "name": name, "labelListVisibility": "labelShow", "messageListVisibility": "show"
    }).execute()
    return new_lb["id"]

def apply_labels(service, msg_id: str, add=None, remove=None):
    service.users().messages().modify(
        userId="me", id=msg_id,
        body={"addLabelIds": add or [], "removeLabelIds": remove or []}
    ).execute()

def reply_flow(dry_run=True, max_results=10):
    service = get_service()
    label_auto = get_or_create_label(service, "AUTO_REPLIED")
    unread = list_unread_messages(service, max_results=max_results)

    results = []
    for m in unread:
        from_h = m["from"]
        if _should_skip(from_h):
            results.append({**m, "category": "SKIPPED", "reason": "blocked sender", "replied": False})
            continue

        # Pick reply-to address from From header
        addr_match = re.search(r"<([^>]+)>", from_h)
        to_addr = addr_match.group(1) if addr_match else from_h

        # Classify
        text_for_cls = f"Subject: {m['subject']}\n\n{m['body'] or m['snippet']}"
        category = classify_email(text_for_cls)
        name = _extract_name(from_h)
        template = TEMPLATES.get(category, TEMPLATES["General Query"])
        reply_text = template.format(name=name)

        # Build the RFC822 reply
        message = build_reply_message(
            to_addr=to_addr,
            subject=m["subject"],
            body_text=reply_text,
            in_reply_to=m.get("message_id",""),
            references=m.get("references","")
        )

        if dry_run:
            # Don’t send; just record what *would* happen
            results.append({**m, "category": category, "replied": False, "reply_to": to_addr, "reply_text": reply_text})
            continue

        # Include threadId in the message body
        message["threadId"] = m["threadId"]
        service.users().messages().send(userId="me", body=message).execute()

        # Mark read + label as AUTO_REPLIED
        apply_labels(service, m["id"], add=[label_auto], remove=["UNREAD"])
        results.append({**m, "category": category, "replied": True, "reply_to": to_addr, "reply_text": reply_text})

    return results

if __name__ == "__main__":
    # First run with dry_run=True to see outputs without sending
    out = reply_flow(dry_run=True, max_results=10)
    for r in out:
        print(r["subject"], "->", r.get("category"), "| replied:", r["replied"])
