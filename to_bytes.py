def to_bytes(massage):
    if isinstance(massage, str):
        massage = massage.encode()
    return massage
