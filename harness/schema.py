from pydantic import BaseModel, Field

class JudgeResult(BaseModel):

    score: int = Field(
        ge=1,
        le=5,
        description="Overall quality score from 1 to 5."
    )

    reason: str = Field(
        min_length=1,
        description="Short explanation for the score."
    )

class EvaluationResult(BaseModel):

    id: str
    customer_message: str
    policy: str
    answer: str

    score: int = Field(
        ge=1,
        le=5
    )

    reason: str
    latency_seconds: float
    estimated_cost: float