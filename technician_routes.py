from fastapi import APIRouter, HTTPException
from database import db
from models import Technician, ServiceRequest
from bson import ObjectId
from datetime import datetime
router = APIRouter()

# Add a new technician
@router.post("/technicians/")
async def add_technician(technician: Technician):
    tech_dict = technician.dict()
    result = await db.technicians.insert_one(tech_dict)
    return {"id": str(result.inserted_id), "message": "Technician added successfully"}

# Get all technicians
@router.get("/technicians/")
async def get_technicians():
    technicians = await db.technicians.find().to_list(100)
    for tech in technicians:
        tech["_id"] = str(tech["_id"])
    return technicians

# Assign a technician to a service request
@router.put("/services/assign/{service_id}")
async def assign_technician(service_id: str, technician_id: str):
    tech = await db.technicians.find_one({"_id": ObjectId(technician_id)})
    if not tech:
        raise HTTPException(status_code=404, detail="Technician not found")

    result = await db.services.update_one(
        {"_id": ObjectId(service_id)}, 
        {"$set": {"assigned_technician": tech["name"], "status": "In Progress"}}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Service request not found")

    return {"message": f"Technician {tech['name']} assigned to service request"}

# Mark a job as completed and update technician performance
@router.put("/services/complete/{service_id}")
async def complete_service(service_id: str):
    service = await db.services.find_one({"_id": ObjectId(service_id)})
    if not service:
        raise HTTPException(status_code=404, detail="Service request not found")

    if service["assigned_technician"]:
        await db.technicians.update_one(
            {"name": service["assigned_technician"]}, 
            {"$inc": {"completed_jobs": 1}}
        )

    await db.services.update_one(
        {"_id": ObjectId(service_id)}, 
        {"$set": {"status": "Completed", "completion_date": datetime.utcnow()}}
    )
    return {"message": "Service marked as completed"}

@router.get("/leaderboard/")
async def get_leaderboard():
    technicians = await db.technicians.find().sort("jobs_completed", -1).to_list(10)
    for tech in technicians:
        tech["_id"] = str(tech["_id"])
    return technicians

@router.post("/rate-technician/")
async def rate_technician(rating: TechnicianRating):
    technician = await db.technicians.find_one({"_id": ObjectId(rating.technician_id)})
    if not technician:
        raise HTTPException(status_code=404, detail="Technician not found")

    # Update average rating
    new_total = technician["total_ratings"] + 1
    new_average = ((technician["average_rating"] * technician["total_ratings"]) + rating.rating) / new_total

    await db.technicians.update_one(
        {"_id": ObjectId(rating.technician_id)},
        {"$set": {"average_rating": new_average, "total_ratings": new_total}}
    )

    await db.technician_ratings.insert_one(rating.dict())

    return {"message": "Rating submitted successfully!"}
