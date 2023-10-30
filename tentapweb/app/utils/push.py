from pywebpush import webpush, WebPushException
import json
from config import Config
import sys


def trigger_push_notification(push_subscription, title, body):
    try:
        response = webpush(
            subscription_info=json.loads(push_subscription.subscription_json),
            data=json.dumps({
                "title": title, 
                "body": body
                }),
            vapid_private_key=Config.VAPID_PRIVATE_KEY,
            vapid_claims={
                "sub": "mailto:{}".format(
                    "example@example.org")
            }
        )
        print(response, file=sys.stderr)
        return response.ok
    except WebPushException as ex:
        print(ex, ex.response, file=sys.stderr)
        if ex.response and ex.response.json():
            extra = ex.response.json()
            print("Remote service replied with a {}:{}, {}",
                  extra.code,
                  extra.errno,
                  extra.message
                  , file=sys.stderr)
        return False


def trigger_push_notifications_for_subscriptions(subscriptions, title, body):
    return [trigger_push_notification(subscription, title, body)
            for subscription in subscriptions]