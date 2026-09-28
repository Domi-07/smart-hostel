from fastapi import FastAPI
from database import engine
from sqlalchemy import text
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
def home() :
    return  {"message": "Smart Hostel сервері жұмыс істеп тұр!"}

@app.get("/rooms")
def get_rooms() :
    with engine.connect() as connection:
        result = connection.execute(text("SELECT * FROM rooms"))
        rooms = result.mappings().all()
        
class RoomCreate(BaseModel):
    room_number: str
    floor: int
    capacity: int
    status: str = "avaiilable"
    
@app.post("/rooms")
def create_room(room: RoomCreate):
    with engine.connect() as connection:
        result = connection.execute(
            text("""
                 INSERT INTRO rooms (room_number, floor, capacity, status)
                 VALUSE (:room_number, :floor, :capacity, :status)
                 RETURNING * """),
            {
                "room_number": room.room_number,
                "floor": room.floor,
                "capacity": room.capacity,
                "status": room.status
            }
        )
        
        connection.commit()
        new_room = result.mappings().one()
        
    return new_room