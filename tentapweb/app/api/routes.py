from flask import request, jsonify
import json

from app.api import bp
from app.models.pushsubscription import PushSubscription
from app.extensions import db
from app.utils.push import trigger_push_notifications_for_subscriptions

@bp.route("/push-subscriptions", methods=["POST"])
def create_push_subscription():
    json_data = request.get_json()
    
    
    subscription_json=json_data['subscription_json']
    
    endpoint = json.loads(subscription_json)['endpoint']
    
    subscription = PushSubscription.query.filter_by(
        subscription_json=json_data['subscription_json']
    ).first()
    if subscription is None:
        subscription = PushSubscription(
            subscription_json=json_data['subscription_json'],
            endpoint = endpoint,
            person_id = 6
        )
        db.session.add(subscription)
        db.session.commit()
    return jsonify({
        "status": "success"
    })
    
@bp.route("/push-unsubscribe", methods=["POST"])
def unsubscribe():
    json_data = request.get_json()
    
    subscription_json = json_data['subscription_json']
    endpoint = json.loads(subscription_json)['endpoint']

    # Find the subscription based on the endpoint
    subscription = PushSubscription.query.filter_by(endpoint=endpoint).first()

    if subscription is not None:
        # If the subscription exists, delete it from the database
        db.session.delete(subscription)
        db.session.commit()
        return jsonify({
            "status": "unsubscribed",
        })
    else:
        # If the subscription doesn't exist, you can return an appropriate error response
        return jsonify({
            "status": "subscription not found",
        })
    
@bp.route("/trigger-push-notifications", methods=["POST"])
def trigger_push_notifications():
    json_data = request.get_json()
    subscriptions = PushSubscription.query.all()
    results = trigger_push_notifications_for_subscriptions(
        subscriptions,
        json_data.get('title'),
        json_data.get('body')
    )
    return jsonify({
        "status": "success",
        "result": results
    })
 