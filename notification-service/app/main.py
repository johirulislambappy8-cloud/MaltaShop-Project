from fastapi import FastAPI

app = FastAPI(title="MaltaShop Notification Service")

@app.get("/")
def home():
    return {"message": "Notification Service is running"}

@app.get("/health")
def health():
    return {"status": "ok"}