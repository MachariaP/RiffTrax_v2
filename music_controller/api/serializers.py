from rest_framework import serializers
from .models import Room


class RoomSerializer(serializers.ModelSerializer):
    """
    Serializer for the Room model.

    Serializes all fields of the Room model, including:
    - id
    - code
    - host
    - guest_can_pause
    - votes_to_skip
    - created_at
    """
    class Meta:
        model = Room
        fields = (
            'id', 'code', 'host', 'guest_can_pause',
            'votes_to_skip', 'created_at'
        )


class CreateRoomSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a Room.

    Serializes only the guest_can_pause and votes_to_skip fields.
    """
    class Meta:
        model = Room
        fields = ('guest_can_pause', 'votes_to_skip')


class UpdateRoomSerializer(serializers.ModelSerializer):
    """
    Serializer for updating a Room.

    Serializes the guest_can_pause, votes_to_skip, and code fields.
    The code field has an empty list of validators to bypass default validation.
    """
    code = serializers.CharField(validators=[])

    class Meta:
        model = Room
        fields = ('guest_can_pause', 'votes_to_skip', 'code')