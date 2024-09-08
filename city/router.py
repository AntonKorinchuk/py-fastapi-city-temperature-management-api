from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from city import crud, schemas
from dependencies import get_db

router = APIRouter()

@router.get("/cities/", response_model=list[schemas.City])
async def read_cities(db: Session = Depends(get_db)) -> list[schemas.City]:
    return crud.get_cities_list(db=db)


@router.post("/cities/", response_model=schemas.City, status_code=status.HTTP_201_CREATED)
async def create_city(
    city: schemas.CityCreate,
    db: Session = Depends(get_db)
) -> schemas.City:
    return crud.create_city(db=db, city=city)


@router.get("/cities/{city_id}/", response_model=schemas.City)
async def read_city(
    city_id: int,
    db: Session = Depends(get_db)
) -> schemas.City:
    db_city = crud.get_city_by_id(db=db, city_id=city_id)
    if db_city is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="City not found")
    return db_city


@router.put("/cities/{city_id}/", response_model=schemas.City)
async def update_city(
    city_id: int,
    city: schemas.CityUpdate,
    db: Session = Depends(get_db)
) -> schemas.City:
    db_city = crud.update_city_by_id(db=db, city_id=city_id, city=city)
    if db_city is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="City not found")
    return db_city


@router.delete("/cities/{city_id}/", response_model=schemas.City)
async def delete_city(
    city_id: int,
    db: Session = Depends(get_db)
) -> schemas.City:
    db_city = crud.delete_city_by_id(db=db, city_id=city_id)
    if db_city is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="City not found")
    return db_city
