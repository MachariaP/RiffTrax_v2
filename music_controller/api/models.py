from django.db import models
import string
import random


def generate_unique_code():
    """
    Generates a unique code consisting of uppercase ASCII letters.

    The function generates a code of length 6 and ensures that the code
    is unique by checking against existing Room objects in the database.

    Returns:
        str: A unique code of length 6.
    """
    length = 6

    while True:
        code = ''.join(random.choices(string.ascii_uppercase, k=length))
        if Room.objects.filter(code=code).count() == 0:
            break

    return code


class Room(models.Model):
    """
    Represents a room in the application.

    Attributes:
        code (str): A unique code for the room, defaulting to a generated unique code.
        host (str): The host of the room, must be unique.
        guest_can_pause (bool): Indicates if guests can pause the music, defaults to False.
        votes_to_skip (int): Number of votes required to skip a song, defaults to 1.
        created_at (datetime): The date and time when the room was created, set automatically.
        current_song (str): The current song playing in the room, can be null.
    """
    code = models.CharField(
        max_length=8, default=generate_unique_code, unique=True
    )
    host = models.CharField(max_length=50, unique=True)
    guest_can_pause = models.BooleanField(null=False, default=False)
    votes_to_skip = models.IntegerField(null=False, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    current_song = models.CharField(max_length=50, null=True)