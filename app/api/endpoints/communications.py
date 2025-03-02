from fastapi import APIRouter
from app.models.communications import NewMeasRequest
from app.core.communication_utils import send_email

router = APIRouter()

@router.post("/request_new_measurement")
async def request_new_measurement(new_measurement_request: NewMeasRequest):
    email_body = """
    <!DOCTYPE html>
    <html lang="it">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Misurazioni NutriBot</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f7f7fb;
                color: #333;
                padding: 0;
                margin: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
            }
            .container {
                background-color: #fff;
                padding: 2rem;
                border-radius: 12px;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
                max-width: 600px;
                width: 100%;
                text-align: center;
            }
            h1 {
                font-size: 2rem;
                color: #000;
            }
            p {
                font-size: 1rem;
                color: #555;
            }
            .button {
                background-color: #8b73f6;
                color: white;
                padding: 1rem 2rem;
                font-size: 1rem;
                font-weight: bold;
                border: none;
                border-radius: 25px;
                text-decoration: none;
                display: inline-block;
                margin-top: 1.5rem;
            }
            .button:hover {
                background-color: #7159c1;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Benvenuto su NutriBot!</h1>
            <p>Scopri il nostro nuovo servizio di estrazione delle misure corporee. Con soli due scatti, potrai ottenere le tue misure in pochi istanti!</p>
            <p>Basta cliccare sul pulsante qui sotto e seguire la procedura guidata direttamente dal tuo telefono.</p>
            <a href="#" class="button">Ottieni le tue misure</a>
            <div class="saia-widget-container"></div>
            <script id="saia-mtm-integration" async src="https://mtm-widget.3dlook.me/integration.js" data-public-key="MjQyNw:1toXav:ObuVUMqYrJnQCE7iUaafn-z940CqFETmqCFKA409dCc"></script>
        </div>
    </body>
    </html>
    """
    result = send_email(new_measurement_request.patEmail, "Richiesta di misurazione", email_body)
    return result
