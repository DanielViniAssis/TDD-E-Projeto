from typing import List
from bson import Decimal128
from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query, status
from pydantic import UUID4
from store.core.exceptions import DatabaseInsertError, NotFoundException, InsertionException  # Certifique-se de que essas exceções existem
from store.schemas.product import ProductIn, ProductOut, ProductUpdate, ProductUpdateOut
from store.usecases.product import ProductUsecase

router = APIRouter(tags=["products"])

@router.post(path="/", status_code=status.HTTP_201_CREATED, response_model=ProductOut)
async def post(
    body: ProductIn = Body(...), usecase: ProductUsecase = Depends()
) -> ProductOut:
    try:
        return await usecase.create(body=body)
    except DatabaseInsertError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get(path="/{id}", status_code=status.HTTP_200_OK, response_model=ProductOut)
async def get(
    id: UUID4 = Path(...), usecase: ProductUsecase = Depends()
) -> ProductOut:
    try:
        return await usecase.get(id=id)
    except NotFoundException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado.")

@router.get(path="/", status_code=status.HTTP_200_OK, response_model=List[ProductOut])
async def query(price_min: float = None, price_max: float = None, usecase: ProductUsecase = Depends()) -> List[ProductOut]:
    return await usecase.query(price_min=price_min, price_max=price_max)

@router.patch(path="/{id}", status_code=status.HTTP_200_OK, response_model=ProductUpdateOut)
async def patch(
    id: UUID4 = Path(...),
    body: ProductUpdate = Body(...),
    usecase: ProductUsecase = Depends(),
) -> ProductUpdateOut:
    try:
        return await usecase.update(id=id, body=body)
    except NotFoundException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message)

@router.delete(path="/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(
    id: UUID4 = Path(...), usecase: ProductUsecase = Depends()
) -> None:
    try:
        await usecase.delete(id=id)
    except NotFoundException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado.")

@router.get(path="/filter", status_code=status.HTTP_200_OK, response_model=List[ProductOut])
async def filter_by_price(
    min_price: Decimal128 = Query(...),
    max_price: Decimal128 = Query(...),
    usecase: ProductUsecase = Depends()
) -> List[ProductOut]:
    return await usecase.query_filtered(min_price=min_price, max_price=max_price)