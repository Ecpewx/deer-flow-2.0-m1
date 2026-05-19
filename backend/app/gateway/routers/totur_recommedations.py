import logging

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services.tutor_recommender import tutor_recommender_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["tutor-recommendations"])


class TutorRecommendationFilters(BaseModel):
    school: str | None = None
    title: str | None = None
    has_papers: bool = False
    has_projects: bool = False


class TutorRecommendationRequest(BaseModel):
    query: str = Field(..., min_length=1, description="Research intent or tutor need")
    k: int = Field(default=5, ge=1, le=20)
    filters: TutorRecommendationFilters | None = None
    llm_optional: bool = True
    fetch_web_content: bool = True
    refresh_web_content: bool = False


class TutorRecommendationItem(BaseModel):
    teacher: str
    title: str
    school: str
    research: str
    email: str
    url: str
    score: float
    reason: str
    papers_count: int
    projects_count: int
    tags: list[str]
    webpage_excerpt: str
    web_fetch_status: str


class TutorRecommendationResponse(BaseModel):
    query: str
    recommendations: list[TutorRecommendationItem]
    debug: dict


@router.post("/tutor-recommendations", response_model=TutorRecommendationResponse)
async def recommend_tutors(request: TutorRecommendationRequest) -> TutorRecommendationResponse:
    try:
        recommendations, debug = tutor_recommender_service.recommend(
            query=request.query,
            k=request.k,
            filters=request.filters.model_dump() if request.filters else None,
            llm_optional=request.llm_optional,
            fetch_web_content=request.fetch_web_content,
            refresh_web_content=request.refresh_web_content,
        )
        return TutorRecommendationResponse(
            query=request.query,
            recommendations=[TutorRecommendationItem(**item.__dict__) for item in recommendations],
            debug=debug,
        )
    except Exception as e:
        logger.error("Failed to recommend tutors: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to recommend tutors: {str(e)}")


@router.get("/tutor-recommendations/health")
async def tutor_recommendations_health() -> dict:
    return tutor_recommender_service.health()
