"""
Healthcheck router. Periodically checks if the application is healthy.
"""

from fastapi import APIRouter, status


router = APIRouter(
    prefix='/api/healthcheck',
    tags=['healthcheck']
)


@router.get('/', status_code=status.HTTP_204_NO_CONTENT)
async def healthcheck():
    """
    Healthcheck endpoint.
    @TODO: Implement healthcheck.
    """
    return
