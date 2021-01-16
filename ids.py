import random
import string

ID_LENGTH = 5

generated_ids = set()


def generate():
    new_id = "".join(random.choices(string.ascii_uppercase + string.digits, k=ID_LENGTH))
    return generate() if new_id in generated_ids else new_id
