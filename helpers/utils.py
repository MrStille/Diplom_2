import string
import random


class ApiHelper:

    @staticmethod
    def get_random_email():
        return f"test-{ApiHelper.generate_random_string(4)}-@yandex.ru"

    @staticmethod
    def generate_random_string(length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string