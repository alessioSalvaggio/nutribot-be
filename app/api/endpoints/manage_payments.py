from fastapi import APIRouter, HTTPException, Request
from stripe.api_resources.checkout import Session
from app.core.mongo_logging import log_to_mongo
import datetime
from firebase_admin import firestore
import stripe
import os

router = APIRouter()
STRYPE_API_KEY = os.getenv("STRYPE_API_KEY")

@router.get("/status")
async def get_status(request: Request):
    """
    Endpoint to check the status of the Stripe integration.
    """
    try:
        await log_to_mongo(request.state.user_id, "app/api/endpoints/manage_stripe/get_status", "INFO", "Stripe status checked")
        return {"status": "Stripe integration is active"}
    except Exception as e:
        await log_to_mongo(request.state.user_id, "app/api/endpoints/manage_stripe/get_status", "ERROR", f"Error checking Stripe status: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to check Stripe status")

@router.get("/confirmation/{CheckoutSessionId}")
async def get_payment_confirmation(CheckoutSessionId: str, request: Request):
    """
    Endpoint to retrieve payment details from Stripe, update user data in Firestore, and return the updated data.
    """
    try:
        # Retrieve the checkout session from Stripe
        stripe.api_key = STRYPE_API_KEY  
        session = Session.retrieve(CheckoutSessionId)

        # Extract user ID and payment details from the session
        user_id = request.state.user_id
        payment_status = session.payment_status
        amount_total = session.amount_total
        currency = session.currency
        
        # tokensAvailable: number;
        # tokensUsed: number;
        # type: "monthly" | "yearly" | "token" | "free";

        # Connect to Firestore
        db = firestore.client()
        user_ref = db.collection("users").document(user_id)
        user_doc = user_ref.get()

        if not user_doc.exists:
            await log_to_mongo(request.state.user_id, "app/api/endpoints/manage_stripe/get_payment_details", "ERROR", f"User {user_id} not found in Firestore")
            raise HTTPException(status_code=404, detail="User not found")

        # Update user payment data in Firestore
        payment_data = {
            "method": session.metadata.get("payment_method", "credit_card"),
            "paymentExpiring": datetime.datetime.now() + datetime.timedelta(days=30),
            "paymentDate": datetime.datetime.now(),
            "measurementsAvailable": 10,
            "measurementsUsed": 0,  # Reset measurements used on payment
            "raw_body": session
        }
        user_ref.update(payment_data)

        # Update mongo collection for user payment history
        user_payment_history_ref = db.collection("users").document(user_id)
        payment_history_doc = user_payment_history_ref.get()
        if not payment_history_doc.exists:
            user_payment_history_ref.set({
                "user_id": user_id,
                "payment_history": []
            })
        user_payment_history_ref.update({
            "payment_history": firestore.ArrayUnion([payment_data])
        })
        # Log the successful update
        await log_to_mongo(request.state.user_id, "app/api/endpoints/manage_stripe/get_payment_details", "INFO", f"Payment details updated for user {user_id}")

        return {"message": "Payment details retrieved and user data updated", "data": payment_data}
    except Exception as e:
        await log_to_mongo(request.state.user_id, "app/api/endpoints/manage_stripe/get_payment_details", "ERROR", f"Error retrieving payment details for session {CheckoutSessionId}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving payment details: {str(e)}")
