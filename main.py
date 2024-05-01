import os
from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from src.kafka.producer import KafkaProducerManager
from src.db.database import Database
from src.db.models import Result
from src.settings.db import DBResult

app = FastAPI()
db = Database(os.getenv("DATABASE_URL"))
producer = KafkaProducerManager('kafka:9092')

@app.on_event("startup")
def startup_event():
    db.create_tables()

@app.on_event("shutdown")
def shutdown_event():
    producer.close()

@app.get("/")
def index():
    return {"index": "classification app working"}

@app.get("/results/{message_id}", response_model=DBResult)
def get_classification_result(message_id: int, db_session: Session = Depends(db.get_db)):
    result = db_session.query(Result).filter(Result.id == message_id).first()
    if result is not None:
        return result
    raise HTTPException(status_code=404, detail="Result not found")

@app.get("/results", status_code=200, response_model=List[DBResult])
def read_results(db_session: Session = Depends(db.get_db)):
    query = select(Result)
    result = db_session.execute(query)
    results = result.scalars().all()
    return results


@app.post("/classify/{message}", status_code=200)
def classify_input(message: str):
    producer.send_message('classify-topic', message)
    return {"status": "Message sent to Kafka"}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")
