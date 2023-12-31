import random
import string
from django.utils import timezone

def get_default_due_date():
    return timezone.now() + timezone.timedelta(days=7)

def generate_random_string(length=30):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))
