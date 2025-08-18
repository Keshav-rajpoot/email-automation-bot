import base64, email, re
from typing import Dict, Any, List

SCOPES = [
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/gmail.send",
]

SAFE_QUERY = "is:unread -category:promotions -category:social newer_than:7d"

def _get_header(headers: List[Dict[str, str]], name: str) -> str:
    for h in headers:
        if h.get("name","").lower() == name.lower():
            return h.get("value","")
    return ""

def _decode_part(data: str) -> str:
    return base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")

def _extract_body(payload: Dict[str, Any]) -> str:
    # Prefer text/plain, fallback to text/html stripped, else empty
    if payload.get("body", {}).get("data"):
        return _decode_part(payload["body"]["data"])
    for part in payload.get("parts", []) or []:
        mime = part.get("mimeType","")
        if mime == "text/plain" and part.get("body", {}).get("data"):
            return _decode_part(part["body"]["data"])
    for part in payload.get("parts", []) or []:
        mime = part.get("mimeType","")
        if mime == "text/html" and part.get("body", {}).get("data"):
            html = _decode_part(part["body"]["data"])
            return re.sub("<[^<]+?>", " ", html)
    return ""

def list_unread_messages(service, max_results=10, query: str = SAFE_QUERY):
    res = service.users().messages().list(userId="me", maxResults=max_results, q=query).execute()
    msgs = res.get("messages", [])
    detailed = []
    for m in msgs:
        full = service.users().messages().get(userId="me", id=m["id"], format="full").execute()
        headers = full["payload"]["headers"]
        detailed.append({
            "id": full["id"],
            "threadId": full["threadId"],
            "from": _get_header(headers, "From"),
            "to": _get_header(headers, "To"),
            "subject": _get_header(headers, "Subject") or "(no subject)",
            "message_id": _get_header(headers, "Message-ID"),
            "references": _get_header(headers, "References"),
            "date": _get_header(headers, "Date"),
            "snippet": full.get("snippet",""),
            "body": _extract_body(full.get("payload", {})),
            "labelIds": full.get("labelIds", []),
        })
    return detailed

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os

def get_service():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return build("gmail", "v1", credentials=creds)

