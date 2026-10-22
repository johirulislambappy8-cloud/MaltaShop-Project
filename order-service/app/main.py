from fastapi import FastAPI

app = FastAPI(title="MaltaShop Order Service")

@app.get("/")
def home():
    return {"message": "MaltaShop Order Service is running"}

@app.get("/health")
def health():
    return {"status": "ok"}