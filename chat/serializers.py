from rest_framework import serializers

from chat.models import ChatRoom, Message
from accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'name')


class ChatRoomSerializer(serializers.ModelSerializer):
    members = UserSerializer(read_only=True, many=True)
    created_by = UserSerializer(read_only=True)
    class Meta:
        model = ChatRoom
        fields = ('id', 'name', 'members', 'created_by')


class CreateChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = ('name', 'members', 'created_by')
        extra_kwargs = {'created_by': {'read_only': True}}

    def validate_members(self, members):
        request = self.context.get('request')
        user = request.user

        if not members:
            members = [user]

        if user not in members:
            members.append(user)

        if len(members)<2:
            raise serializers.ValidationError('A Chat Room must have at least two members!')
        
        return members
    
    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user

        validated_data['created_by'] = user

        members = validated_data.pop('members', [])

        chat_room = ChatRoom.objects.create(**validated_data)
        chat_room.members.set(members)

        return chat_room


class UpdateChatRoomMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = ('members',)

    def update(self, instance, validated_data):
        new_members = validated_data.get('members', [])

        for user in new_members:
            instance.members.add(user)

        return instance