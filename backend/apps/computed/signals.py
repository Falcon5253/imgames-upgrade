from django.db.models.signals import post_save, post_delete
from graphene_subscriptions.signals import post_save_subscription, post_delete_subscription

from .models import StageComputed, ChannelComputed

post_save.connect(post_save_subscription, sender=StageComputed,
                  dispatch_uid="stage_computed_post_save")
post_save.connect(post_save_subscription, sender=ChannelComputed,
                  dispatch_uid="channel_computed_post_save")
