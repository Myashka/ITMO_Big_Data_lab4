import os
import time
from contextlib import asynccontextmanager
from typing import List

from fastapi import Depends, FastAPI, HTTPException
from requests import Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.classifier import Classifier
from src.db import models
from src.db.database import engine, get_db
from src.db.models import Result
from src.preprocessor import Preprocessor
from src.settings.classifier import PredictOutput
from src.settings.config import AppConfig
from src.settings.db import DBResult
from src.settings.preprocessor import PreprocessorSettings
from src.utils import load_config


@asynccontextmanager
async def lifespan(app: FastAPI):
    config: AppConfig = load_config()

    assert os.path.isdir(config.load_path), "There is no model dir"

    app.state.preprocessor_settings = PreprocessorSettings(
        **config.preprocessing_config.dict()
    )
    app.state.preprocessor = Preprocessor(settings=app.state.preprocessor_settings)
    app.state.classifier = Classifier.load(config.load_path)

    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
def index():
    return {"index": "classification app working"}


@app.get("/results", status_code=200, response_model=List[DBResult])
async def read_results(db: AsyncSession = Depends(get_db)):
    async with db as session:
        query = select(Result)
        result = await session.execute(query)
        results = result.scalars().all()
        return results


@app.post("/classify/{message}", status_code=200, response_model=PredictOutput)
async def classify_input(message: str, db: AsyncSession = Depends(get_db)):
    try:
        processed_test: str = app.state.preprocessor(message)
        pred: PredictOutput = app.state.classifier.predict(processed_test)
        result = models.Result(message=message, sentiment=pred.sentiment)
        db.add(result)
        await db.commit()
        return pred
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")
