from fastapi import FastAPI
from app.api import base_router
from app.repositories.database import connect_to_mongo, close_mongo_connection

app = FastAPI()

app.add_event_handler("startup", connect_to_mongo)
app.add_event_handler("shutdown", close_mongo_connection)
app.include_router(base_router.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Exam Portal API"}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=4000,
        reload=True,
    )