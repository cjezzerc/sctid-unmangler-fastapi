import os
import datetime

from fastapi import FastAPI, Request
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .unmangling.check_entered_data import check_entered_data

import logging

logger = logging.getLogger("uvicorn.error")
# logging.basicConfig(
#     level=logging.DEBUG,
#     format="%(asctime)s | %(levelname)-8s | "
#     "%(module)s:%(funcName)s:%(lineno)d - %(message)s",
# )

app = FastAPI()

# CORS_ORIGINS env var should be comma separated string of URLs, e.g. 'http://localhost:5173,http://localhost:4173'
if "CORS_ORIGINS" in os.environ:
    origins=os.environ["CORS_ORIGINS"].split(",")
else:
    origins=[]

logger.info(f"CORS origins: {origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ListOfIds(BaseModel):
    ids: list


class ReceivedData(BaseModel):
    entered_text: str
    did_ignore_flag: bool = False


@app.get("/health")
def health_check():
    return f"healthy at {datetime.datetime.now()}"


@app.post("/receive_entered_data")
def receive_entered_data(request: Request, received_data: ReceivedData):
    snomed_release=os.environ["DESCRIPTIONS_SQLLITE_FILE"].split("_")[-1][:-3]
    logger.info(f"headers: {request.headers}")
    return {
        "metadata": {"snomed_release":snomed_release},
        "check_results": check_entered_data(
            text=received_data.entered_text,
            did_ignore_flag=received_data.did_ignore_flag,
        )
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
