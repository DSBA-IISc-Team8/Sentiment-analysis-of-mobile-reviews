from fastapi import FastAPI
from pydantic import BaseModel
from loguru import logger
from fastapi.middleware.cors import CORSMiddleware

from app.predict import get_predictions

# Creating FastAPI instance
app = FastAPI()

origins = [
    "http://localhost:3000",
    "localhost:3000"
]

# Add cross origin support
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def root():

  result = {"message": "Check swagger docs http://localhost:8000/docs"}
  return result


# ==========================================================================================================================


# Creating class to define the request body
# and the type hints of each attribute
class request_body(BaseModel):
	text : str


# Creating an Endpoint to receive the data
# to make prediction on.
@app.post('/predict')
def predict(data : request_body):

  logger.info(data)

  # Making the data in a form suitable for prediction
  text = data.text

  # Predicting
  response = get_predictions(text)

  # Return the Result
  return response