from fastapi import APIRouter, HTTPException, Depends
from database import db
from models import Product
from auth import get_current_user
from bson import ObjectId

router = APIRouter()

@router.post("/products/")
async def add_product(product: Product, user=Depends(get_current_user)):
    product_dict = product.dict()
    result = await db.products.insert_one(product_dict)
    return {"id": str(result.inserted_id), "message": "Product added successfully"}

@router.get("/products/")
async def get_products():
    products = await db.products.find().to_list(100)
    for product in products:
        product["_id"] = str(product["_id"])
    return products

@router.get("/products/{product_id}")
async def get_product(product_id: str):
    product = await db.products.find_one({"_id": ObjectId(product_id)})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    product["_id"] = str(product["_id"])
    return product

@router.put("/products/{product_id}")
async def update_product(product_id: str, updated_product: Product, user=Depends(get_current_user)):
    product_dict = updated_product.dict()
    result = await db.products.update_one({"_id": ObjectId(product_id)}, {"$set": product_dict})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Product not found or no changes made")
    return {"message": "Product updated successfully"}

@router.delete("/products/{product_id}")
async def delete_product(product_id: str, user=Depends(get_current_user)):
    result = await db.products.delete_one({"_id": ObjectId(product_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}
