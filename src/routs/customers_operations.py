from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.database.models import Vessel
from fastapi.responses import JSONResponse
from fastapi import status
from src.database.db import get_db
from src.vessels_operations.operations import get_or_create_vessel

router = APIRouter(prefix="/customers_operation", tags=["vessels_operations"])

@router.get("/get-vessel/")
async def add_vessel(imo_or_mmsi: str, db: AsyncSession = Depends(get_db)):
    res = await get_or_create_vessel(imo_or_mmsi, db)
    return {'res': res}
