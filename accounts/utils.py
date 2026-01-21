import secrets
import string


def generate_password(length=10):
    char=string.ascii_letters + string.digits
    password=''.join(secrets.choice(char) for _ in range(length))
    return password