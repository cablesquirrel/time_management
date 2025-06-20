"""Program Entry Point"""

import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from index import router
from logger import CustomLogger
from time_manager import TimeManager
from logging import INFO

logger = CustomLogger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """FastAPI lifespan task to run the TimeManager."""
    # Create a TimeManager instance
    time_manager = TimeManager.get_instance()
    task = asyncio.create_task(time_manager.run())
    logger.log(INFO, "Timer loop started.")
    yield
    logger.log(INFO, "Shutting down timer...")
    await time_manager.shutdown()
    await task


# Create the FastAPI instance
app = FastAPI(title="Time Management", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)


@app.get("/")
def read_root() -> dict:
    """
    Return API response for root directory.

    Returns:
        dict: default message back to user

    """
    return {"Message": "Hello from Time Management!"}


def main():
    pass


if __name__ == "__main__":
    main()
