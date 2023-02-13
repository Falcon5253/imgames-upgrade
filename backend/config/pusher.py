import pusher
from .settings import env

APP_ID = env.str('PUSHER_APP_ID')
KEY = env.str('PUSHER_KEY')
SECRET = env.str('PUSHER_SECRET')
CLUSTER = env.str('PUSHER_CLUSTER')

pusher_client = pusher.Pusher(
  app_id=APP_ID,
  key=KEY,
  secret=SECRET,
  cluster=CLUSTER,
  ssl=True
)