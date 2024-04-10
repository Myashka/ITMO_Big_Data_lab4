import os
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Path
from requests import Request

from src.classifier import Classifier
from src.preprocessor import Preprocessor
from src.settings.classifier import PredictOutput
from src.settings.config import AppConfig
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

    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def index():
    return {"index": "classification app working"}


@app.get("/classify/{message}", status_code=200, response_model=PredictOutput)
def classify_input(
    message: str = Path(..., description="The message to classify.")
) -> PredictOutput:
    try:
        processed_test: str = app.state.preprocessor(message)
        pred: PredictOutput = app.state.classifier.predict(processed_test)
        return pred
    except Exception as e:
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
