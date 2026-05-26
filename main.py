import logging

import uvicorn
from fastapi import FastAPI

from api.routes import router
from config.settings import settings

logging.basicConfig(level=getattr(logging, settings.log_level.upper()))

app = FastAPI(title="Email Agent", version="1.0.0")
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
