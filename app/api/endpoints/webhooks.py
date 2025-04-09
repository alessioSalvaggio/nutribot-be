from fastapi import APIRouter, HTTPException, Request

router = APIRouter()

@router.post("/errors")
async def error_webhook(request: Request):
    """
    Centralized webhook to handle error notifications.
    """
    try:
        error_data = await request.json()
        # Esegui azioni con i dati dell'errore, ad esempio:
        # - Inviare un'email
        # - Inviare un messaggio su Slack
        # - Creare un ticket di supporto
        print(f"Received error notification: {error_data}")
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process webhook: {str(e)}")
