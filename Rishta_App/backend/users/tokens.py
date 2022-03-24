import string
import random


class TokenGenerator():
    @staticmethod
    def generate_token(size=4, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))


