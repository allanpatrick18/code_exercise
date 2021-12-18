import uvicorn
from typing import List
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
app = FastAPI()
import model
from sports_book.view import *


@app.get("/")
async def read_main():
    return {"msg": "Sever Up!"}


"""
Sports API
"""

@app.get("/sports/{sport_id}", response_model=model.Sport)
async def read_sport(sport_id: int):
    return get_objects_by_id('sports', sport_id)


@app.get("/sports/", response_model=List[model.Sport])
async def read_all_sports():
    return get_all_objects('sports')


@app.put("/sports/{sport_id}", response_model=model.Sport)
async def update_sport(sport_id: str, item: model.Sport):
    update_item_encoded = jsonable_encoder(item)
    sport_obj = Sport.parse_obj(update_item_encoded)
    create_update_sports(sport_obj, sport_id)
    return update_item_encoded


@app.post("/sports/", response_model=model.Sport)
async def update_sport(sport: model.Sport):
    update_item_encoded = jsonable_encoder(sport)
    sport_obj = Sport.parse_obj(update_item_encoded)
    create_update_sports(sport_obj)
    return update_item_encoded

"""
Event API
"""

@app.get("/events/{event_id}", response_model=model.EventIn)
async def read_events(event_id: int):
    return get_objects_by_id('events', event_id)


@app.get("/events/", response_model=List[model.EventIn])
async def read_all_events():
    return get_all_objects('events')


@app.put("/events/{event_id}", response_model=model.Event)
async def update_events(event_id: int, item: model.Event):
    update_item_encoded = jsonable_encoder(item)
    event = model.Event.parse_obj(update_item_encoded)
    event = create_update_event(event)
    return event


@app.post("/events/", response_model=model.EventIn)
async def create_events(item: model.Event):
    update_item_encoded = jsonable_encoder(item)
    event = model.Event.parse_obj(update_item_encoded)
    event = create_update_event(event)
    return event


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)