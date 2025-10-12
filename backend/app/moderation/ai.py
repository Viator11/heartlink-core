BANNED = {"spam","scam","xxx","porn","viagra","nazi"}

def moderate_text(text: str) -> bool:
    """True = разрешено, False = запрещено."""
    if not text:
        return True
    t = text.lower()
    return not any(w in t for w in BANNED)