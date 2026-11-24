
from pydantic import BaseModel, Field


class ReviewRequest(BaseModel):
    repository_name: str = Field(
        min_length=1,
        max_length=200
    )

    diff_text: str = Field(
        min_length=1
    )


class ReviewResponse(BaseModel):
    review_id: int
    repository_name: str
    status: str
    recommendation: str | None = None
    final_report: str | None = None
