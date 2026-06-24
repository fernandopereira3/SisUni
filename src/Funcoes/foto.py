import base64


def foto_para_base64(valor):
    if not valor:
        return None
    try:
        if isinstance(valor, str):
            return valor  # já convertido
        b = bytes(valor)
        if len(b) < 4:
            return None
        # Valida magic bytes JPEG ou PNG
        if b[:2] != b"\xff\xd8" and b[:4] != b"\x89PNG":
            return None
        return base64.b64encode(b).decode("utf-8")
    except Exception:
        return None
