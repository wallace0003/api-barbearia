from __future__ import annotations
import uvicorn
from fastapi import FastAPI
from src.api.router import api_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="La Boina Barbearia",
    version="0.0.1",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.get("/")
async def root():
    return {"ping":"pong"}

if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        host="127.0.0.1",
        port=8080,
        reload=True,
    )
