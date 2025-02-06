from fastapi import APIRouter, HTTPException, Depends
from database import db
from models import ServiceRequest
from auth import get_current_user
from bson import ObjectId

router = APIRouter()

# Submit a new service request
@router.post("/services/")
async def create_service_request(service: ServiceRequest):
    service_dict = service.dict()
    result = await db.services.insert_one(service_dict)
    return {"id": str(result.inserted_id), "message": "Service request submitted successfully"}

# Get all service requests (Admin/Technician only)
@router.get("/services/")
async def get_all_services(user=Depends(get_current_user)):
    services = await db.services.find().to_list(100)
    for service in services:
        service["_id"] = str(service["_id"])
    return services

# Get a specific service request by ID
@router.get("/services/{service_id}")
async def get_service(service_id: str):
    service = await db.services.find_one({"_id": ObjectId(service_id)})
    if not service:
        raise HTTPException(status_code=404, detail="Service request not found")
    service["_id"] = str(service["_id"])
    return service

# Update service request status (Admin/Technician)
@router.put("/services/{service_id}")
async def update_service_status(service_id: str, status: str, user=Depends(get_current_user)):
    result = await db.services.update_one({"_id": ObjectId(service_id)}, {"$set": {"status": status}})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Service request not found")
    return {"message": f"Service status updated to {status}"}

# Delete a service request (Admin only)
@router.delete("/services/{service_id}")
async def delete_service(service_id: str, user=Depends(get_current_user)):
    result = await db.services.delete_one({"_id": ObjectId(service_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Service request not found")
    return {"message": "Service request deleted successfully"}

@router.get("/admin/services/")
async def get_services_dashboard(status: str = None, user=Depends(get_current_user)):
    query = {}
    if status:
        query["status"] = status  # Filter by status if provided

    services = await db.services.find(query).to_list(100)
    for service in services:
        service["_id"] = str(service["_id"])
    return services

@router.put("/services/assign/{service_id}")
async def assign_technician(service_id: str, technician_id: str, user=Depends(get_current_user)):
    technician = await db.technicians.find_one({"_id": ObjectId(technician_id)})
    if not technician:
        raise HTTPException(status_code=404, detail="Technician not found")

    result = await db.services.update_one(
        {"_id": ObjectId(service_id)}, {"$set": {"technician_id": technician_id, "status": "Assigned"}}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Service request not found")

    return {"message": f"Service assigned to {technician['name']}"}

@router.put("/services/complete/{service_id}")
async def complete_service(service_id: str, user=Depends(get_current_user)):
    service = await db.services.find_one({"_id": ObjectId(service_id)})
    if not service:
        raise HTTPException(status_code=404, detail="Service request not found")

    if service.get("technician_id"):
        await db.technicians.update_one(
            {"_id": ObjectId(service["technician_id"])}, {"$inc": {"jobs_completed": 1}}
        )

    await db.services.update_one({"_id": ObjectId(service_id)}, {"$set": {"status": "Completed"}})
    
    return {"message": "Service marked as completed and technician rating updated"}
