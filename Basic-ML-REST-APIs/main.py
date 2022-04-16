import uvicorn
from loguru import logger

logger.add('rest.log', rotation="10 MB")

def start():

  logger.info("Server Stared")

  uvicorn.run("app.api:app", host="0.0.0.0", port=8000, log_level="debug", reload=True)

if __name__ == "__main__":

  logger.info("Main script")
  start()