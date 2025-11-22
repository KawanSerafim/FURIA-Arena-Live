from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.routers import websocket_router
import os

app = FastAPI(
    title="FURIA Arena",
    description="API de Chat Real-Time com IA Generativa para torcedores.",
    version="1.0.2"
)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(websocket_router.router)

@app.get("/")
async def read_root():
    return FileResponse("static/index.html")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port)