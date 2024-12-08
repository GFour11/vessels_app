from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.database.models import Vessel
from src.database.db import get_db
from src.vessels_operations.operations import get_or_create_vessel

router = APIRouter(prefix="/customers_operation", tags=["vessels_operations"])

@router.get("/get-vessel/")
async def add_vessel(imo_or_mmsi: str, db: AsyncSession = Depends(get_db)):
    res = await get_or_create_vessel(imo_or_mmsi, db)
    # result = await db.execute(select(Vessel).where(Vessel.imo == imo))
    # vessel = result.scalars().first()
    #
    # if vessel:
    #     return {"message": f"Vessel with IMO {imo} already exists."}
    #
    # new_vessel = Vessel(imo=imo)
    # db.add(new_vessel)
    # await db.commit()
    return res