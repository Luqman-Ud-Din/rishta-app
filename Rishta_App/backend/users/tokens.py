import string
import random


class TokenGenerator():
    @staticmethod
    def generate_token(size=4):
        chars = string.ascii_uppercase
        numbers = string.digits
        total_digits = random.choice([num for num in range(size-1)])
        chars_collection = [random.choice(chars) for _ in range(size-total_digits)]
        digits_collection = [random.choice(numbers) for _ in range(total_digits)]

        return ''.join(chars_collection + digits_collection)
