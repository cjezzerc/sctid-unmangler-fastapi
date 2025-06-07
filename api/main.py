import datetime

from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .unmangling.check_entered_data import check_entered_data

import logging

logger = logging.getLogger("my_logger")
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)-8s | "
    "%(module)s:%(funcName)s:%(lineno)d - %(message)s",
)

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://localhost:4173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ListOfIds(BaseModel):
    ids: list


class EnteredData(BaseModel):
    text: str


# @app.post("/check_many/")
# def check_many(sctids: ListOfIds):
#     return do_checks(sctids.ids)


@app.get("/health")
def health_check():
    return f"healthy at {datetime.datetime.now()}"


@app.post("/receive_entered_data/")
def receive_entered_data(entered_data: EnteredData):
    return {"check_results": check_entered_data(text=entered_data.text)}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
