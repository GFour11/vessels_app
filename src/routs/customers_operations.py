from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.db import get_db
from src.vessels_operations.operations import get_or_create_vessel

router = APIRouter(prefix="/customers_operation", tags=["vessels_operations"])

@router.get("/get-vessel/")
async def add_vessel(imo_or_mmsi: str, db: AsyncSession = Depends(get_db)):
    """Get router. return info about current ship.
    params:
    imo_or_mmsi: str IMO or MMSI number of ship
    return JSON data."""
    res = await get_or_create_vessel(imo_or_mmsi, db)
    return {'res': res}
