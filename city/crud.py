from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy.future import select

from city import schemas
from city.models import DBCity


async def get_cities_list(db: Session) -> list[DBCity]:
    result = await db.execute(select(DBCity))
    return result.scalars().all()


async def get_city_by_id(db: Session, city_id: int) -> Optional[DBCity]:
    result = await db.execute(select(DBCity).filter(DBCity.id == city_id))
    return result.scalars().first()


async def create_city(db: Session, city: schemas.CityCreate) -> DBCity:
    db_city = DBCity(
        name=city.name,
        additional_info=city.additional_info,
    )
    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)
    return db_city


async def update_city_by_id(
        db: Session,
        city_id: int,
        city: schemas.CityUpdate
) -> Optional[DBCity]:
    db_city = await get_city_by_id(db=db, city_id=city_id)
    if db_city:
        if city.name:
            db_city.name = city.name
        if city.additional_info:
            db_city.additional_info = city.additional_info
        await db.commit()
        await db.refresh(db_city)
    return db_city


async def delete_city_by_id(db: Session, city_id: int) -> Optional[DBCity]:
    db_city = await get_city_by_id(db=db, city_id=city_id)
    if db_city:
        await db.delete(db_city)
        await db.commit()
    return db_city