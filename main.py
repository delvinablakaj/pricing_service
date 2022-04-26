from fastapi import FastAPI
from routes import pricing

app = FastAPI()


app.include_router(pricing.router)