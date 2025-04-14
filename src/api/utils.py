"""Utils api view"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from src.database.db import get_db
from src.schemas.utils import HealthCheckModel, HealthCheckErrorModel
from src.exceptions.utils import DatabaseConfigError, DatabaseConnectionError

router = APIRouter(tags=["utils"])


@router.get(
    "/healthchecker",
    response_model=HealthCheckModel,
    responses={
        500: {"model": HealthCheckErrorModel, "description": "Database error"},
    },
)
async def healthchecker(db: AsyncSession = Depends(get_db)):
    """Health check"""
    try:
        result = await db.execute(text("SELECT 1"))
        result = result.scalar_one_or_none()

        if result is None:
            raise DatabaseConfigError
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        raise DatabaseConnectionError from e
