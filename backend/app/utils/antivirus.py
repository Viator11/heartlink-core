import clamd

def scan_bytes(data: bytes) -> bool:
    """Возвращает True, если файл чистый или ClamAV недоступен (dev-режим)."""
    try:
        cd = clamd.ClamdNetworkSocket()  # по умолчанию clamav:3310 из docker-compose
        res = cd.instream(data)
        status = list(res.values())[0][0] if isinstance(res, dict) else "OK"
        return status == "OK"
    except Exception:
        # Не валим загрузку в dev, если ClamAV ещё не поднялся
        return True