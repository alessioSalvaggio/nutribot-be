from fastapi.middleware.cors import CORSMiddleware

def add_cors_middleware(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "https://hypaz.com",
            "https://www.hypaz.com",
            "https://nutribot.it",
            "https://www.nutribot.it",
            "http://193.168.75.86",
            "https://193.168.75.86"
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
