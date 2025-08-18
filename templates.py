TEMPLATES = {
    "Billing Issue": (
        "Hi {name},\n\nThanks for reaching out. I’ve noted this as a billing-related query. "
        "Please share your order ID and billing email so we can investigate and revert.\n\nRegards,\nSupport"
    ),
    "Technical Support": (
        "Hi {name},\n\nThanks for contacting us. I’ve logged this as a technical issue. "
        "Please share steps to reproduce, screenshots, and any error messages.\n\nRegards,\nSupport"
    ),
    "General Query": (
        "Hi {name},\n\nThanks for writing in. We’ve received your query and will get back shortly.\n\nRegards,\nSupport"
    ),
}

BLOCKLIST_SENDERS = ["no-reply", "noreply", "mailer-daemon", "postmaster"]
