import random

def generate_password(password_length: int) -> str:
    chars = 'abcdefghijklmnopqrstuvwxyz1234567890~`!@#$%^&*()_-+={[}]|\\:;<,>.?ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    password = ''.join(random.choice(chars) for _ in range(password_length))
    return password