from typing import List, Annotated

from fastapi import APIRouter, HTTPException, Depends, Request

from app.schema.f1api import Drivers, Teams

from app.common.f1api import F1Scraper

from app.dependencies import get_current_user
from app.routes.root import limiter


f1api = F1Scraper()

router = APIRouter(prefix="/v1", tags=["f1"])


@router.get("/f1drivers")
@limiter.limit("5/minute")
async def f1drivers(
    request: Request,
    current_user: Annotated[str, Depends(get_current_user)] = None,
) -> List[Drivers]:
    try:
        data = f1api.get_driver_data()
        data_items = []
        if data:
            driver_data = data["data"]
            data_items = [Drivers(**item) for item in driver_data]
        return data_items
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/f1teams")
async def f1teams(
    request: Request,
    current_user: Annotated[str, Depends(get_current_user)] = None,
) -> List[Teams]:
    try:
        data_items = []
        data = f1api.get_team_data()
        if data:
            team_data = data["data"]
            data_items = [Teams(**item) for item in team_data]
        return data_items
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
