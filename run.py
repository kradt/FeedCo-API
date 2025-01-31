import uvicorn
from src import config


if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=config.DEBUG)
