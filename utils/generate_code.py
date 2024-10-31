import string
import random


# This function is for generating code for every order
def generate_code(n=8):
    text = string.digits + string.ascii_uppercase + string.digits
    code = ''.join([random.choice(text) for _ in range(n)])
    return code


def user_activation_code(n=6):
    text = string.digits
    code = ''.join([random.choice(text) for _ in range(n)])
    return code