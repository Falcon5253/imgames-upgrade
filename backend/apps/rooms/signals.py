from django.db.models.signals import post_save, post_delete
from graphene_subscriptions.signals import post_save_subscription, post_delete_subscription

from apps.rooms.models import Room, Round, RoomParticipant, Message, Queue

post_save.connect(post_save_subscription, sender=Room,
                  dispatch_uid="room_post_save")
post_save.connect(post_save_subscription, sender=Round,
                  dispatch_uid="round_post_save")
post_save.connect(post_save_subscription, sender=RoomParticipant,
                  dispatch_uid="room_participant_post_save")
post_save.connect(post_save_subscription, sender=Message,
                  dispatch_uid="room_message_post_save")
post_save.connect(post_save_subscription, sender=Queue,
                  dispatch_uid="room_queue_post_save")
post_save.connect(post_save_subscription, sender=Round,
                  dispatch_uid="room_round_activity_save")