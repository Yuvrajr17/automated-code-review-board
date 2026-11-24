from contextlib import asynccontextmanager

from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.schemas.review_request import ReviewRequest
from app.schemas.review_request import ReviewResponse
from app.workflows.review_service import execute_review



from fastapi import FastAPI

from app.database.connection import initialize_database


@asynccontextmanager
async def lifespan(app: FastAPI):

    # Initialize database when application starts
    initialize_database()

    yield

    # Application shutdown logic can go here


app = FastAPI(
    title="Automated Code Review Board",
    description="AI-powered Multi-Agent Code Review System",
    version="0.1.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():

    return {
        "message": "Automated Code Review Board API is running"
    }


@app.get("/health")
def health_check():

    return {
        "status": "healthy",
        "project": "Automated Code Review Board"
    }


@app.get("/db-status")
def database_status():

    from app.database.connection import db_connection

    with db_connection() as connection:

        cursor = connection.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            AND name NOT LIKE 'sqlite_%'
        """)

        tables = [row["name"] for row in cursor.fetchall()]

    return {
        "database": "SQLite",
        "status": "connected",
        "tables": tables
    }



@app.post("/reviews", response_model=ReviewResponse)
async def create_review(request: ReviewRequest):

    try:
        result = await execute_review(
            repository_name=request.repository_name,
            diff_text=request.diff_text
        )

        return result

    except Exception as error:
        import traceback

        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


@app.get("/reviews/{review_id}")
def get_review(review_id: int):

    from app.database.connection import db_connection

    with db_connection() as connection:

        review = connection.execute(
            "SELECT * FROM reviews WHERE id = ?",
            (review_id,)
        ).fetchone()

        if review is None:
            raise HTTPException(
                status_code=404,
                detail="Review not found"
            )

        logs = connection.execute(
            """
            SELECT agent_name, status, output
            FROM agent_logs
            WHERE review_id = ?
            """,
            (review_id,)
        ).fetchall()

    return {
        "review": dict(review),
        "agent_logs": [dict(log) for log in logs]
    }
