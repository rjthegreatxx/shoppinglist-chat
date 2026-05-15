import logging

import stripe
from fastapi import APIRouter, HTTPException, Request

from app.config import settings
from app.models.schemas import CheckoutRequest, CheckoutResponse

router = APIRouter()
logger = logging.getLogger(__name__)


def _price_cents(product_id: str) -> int:
    try:
        num = int(product_id.split("-")[1])
    except (IndexError, ValueError):
        num = 1
    return (num % 10 + 1) * 499


@router.post("/checkout", response_model=CheckoutResponse)
async def create_checkout(request: CheckoutRequest) -> CheckoutResponse:
    if not settings.stripe_secret_key:
        raise HTTPException(status_code=503, detail="Stripe not configured")

    stripe.api_key = settings.stripe_secret_key

    line_items = [
        {
            "price_data": {
                "currency": "usd",
                "unit_amount": _price_cents(item.product_id),
                "product_data": {"name": item.name},
            },
            "quantity": item.quantity,
        }
        for item in request.items
    ]

    try:
        session = stripe.checkout.Session.create(
            mode="payment",
            line_items=line_items,
            success_url=settings.stripe_success_url,
            cancel_url=settings.stripe_cancel_url,
        )
        return CheckoutResponse(url=session.url)
    except stripe.StripeError as e:
        logger.exception("Stripe session creation failed")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/webhook")
async def stripe_webhook(request: Request) -> dict:
    payload = await request.body()
    sig = request.headers.get("stripe-signature", "")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig, settings.stripe_webhook_secret
        )
    except (ValueError, stripe.SignatureVerificationError):
        raise HTTPException(status_code=400, detail="Invalid webhook")

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        logger.info("Payment completed session_id=%s", session["id"])

    return {"received": True}
