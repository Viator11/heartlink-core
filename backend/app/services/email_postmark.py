import http.client
import json
import os

POSTMARK_TOKEN = os.getenv("POSTMARK_API_TOKEN") or os.getenv("SMTP_USER")
FROM_EMAIL = os.getenv("SMTP_FROM", "noreply@heartlink.love")

def send_verify_email(email: str, username: str | None, verify_link: str, lang: str = "ru"):
    if not POSTMARK_TOKEN:
        print("[WARN] Postmark token missing — email not sent")
        return False

    payload = {
        "From": f"HeartLink ❤ ️ <{FROM_EMAIL}>",
        "To": email,
        "TemplateAlias": "verify-email",
        "TemplateModel": {
            "lang": lang,
            "username": username or "",
            "verify_link": verify_link
        }
    }
    conn = http.client.HTTPSConnection("api.postmarkapp.com")
    conn.request("POST", "/email/withTemplate",
                 body=json.dumps(payload).encode("utf-8"),
                 headers={
                     "Accept": "application/json",
                     "Content-Type": "application/json",
                     "X-Postmark-Server-Token": POSTMARK_TOKEN
                 })
    res = conn.getresponse()
    ok = 200 <= res.status < 300
    if not ok:
        print("[ERROR] Postmark send failed", res.status, res.read())
    return ok
