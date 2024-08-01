from datetime import datetime
from typing import List
from uuid import UUID
from bson import Decimal128
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
import pymongo
from store.db.mongo import db_client
from store.models.product import ProductModel
from store.schemas.product import ProductIn, ProductOut, ProductUpdate, ProductUpdateOut
from store.core.exceptions import DatabaseInsertError, NotFoundException

class ProductUsecase:
    def __init__(self) -> None:
        self.client: AsyncIOMotorClient = db_client.get()
        self.database: AsyncIOMotorDatabase = self.client.get_database()
        self.collection = self.database.get_collection("products")
        
    async def create(self, body: ProductIn) -> ProductOut:
        product_model = ProductModel(**body.model_dump())
        try:
            await self.collection.insert_one(product_model.model_dump())
        except pymongo.errors.PyMongoError as e: 
            raise DatabaseInsertError("Erro ao inserir o produto. Verifique os dados fornecidos.")
        except Exception as e:  
            raise DatabaseInsertError(str(e))

        return ProductOut(**product_model.model_dump())

    async def get(self, id: UUID) -> ProductOut:
        result = await self.collection.find_one({"id": id})

        if not result:
            raise NotFoundException(message=f"Product not found with filter: {id}")

        return ProductOut(**result)

    async def query(self, price_min: float = None, price_max: float = None) -> List[ProductOut]:
        query = {}
        if price_min is not None:
            query["price"] = {"$gt": price_min}
        if price_max is not None:
            if "price" not in query:
                query["price"] = {}
            query["price"]["$lt"] = price_max

        return [ProductOut(**item) async for item in self.collection.find(query)]
    
    async def query_filtered(self, min_price: Decimal128, max_price: Decimal128) -> List[ProductOut]:
        cursor = self.collection.find({
            "price": {"$gt": min_price, "$lt": max_price}
        })
        return [ProductOut(**item) async for item in cursor]

    
    async def update(self, id: UUID, body: ProductUpdate) -> ProductUpdateOut:
        body_dict = body.model_dump(exclude_none=True)
        body_dict['updated_at'] = datetime.now()

        result = await self.collection.find_one_and_update(
            filter={"id": id},
            update={"$set": body_dict},
            return_document=pymongo.ReturnDocument.AFTER,
        )

        if not result:
            raise NotFoundException(message=f"Product not found with filter: {id}")

        return ProductUpdateOut(**result)

    async def delete(self, id: UUID) -> bool:
        product = await self.collection.find_one({"id": id})
        if not product:
            raise NotFoundException(message=f"Product not found with filter: {id}")

        result = await self.collection.delete_one({"id": id})

        return True if result.deleted_count > 0 else False

product_usecase = ProductUsecase()
