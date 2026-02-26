from fastapi import APIRouter

router = APIRouter(
    prefix="/billing",
    tags=["Billing"]
)


@router.get("/plans")
def get_plans():
    return {
        "FREE": {
            "price": 0,
            "features": [
                "Planner",
                "Limited Questions",
                "Limited AI Explanations"
            ]
        },
        "PRO": {
            "price": 299,
            "features": [
                "Unlimited Questions",
                "Unlimited AI",
                "Adaptive Priority",
                "Detailed Feedback"
            ]
        }
    }