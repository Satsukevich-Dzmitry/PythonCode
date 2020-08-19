def to_bytes(massage: str) -> bytes:
    if isinstance(massage, str):
        massage = massage.encode()
    return massage
