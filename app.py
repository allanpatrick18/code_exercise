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


@app.get("/sports/{sport_id}", response_model=model.Sports)
async def read_sport(sport_id: int):
    return get_objects_by_id('sports', sport_id)


@app.get("/sports/", response_model=List[model.Sports])
async def read_all_sports():
    return get_all_objects('sports')


@app.put("/sports/{sport_id}", response_model=model.Sports)
async def update_sport(sport_id: str, item: model.Sports):
    update_item_encoded = jsonable_encoder(item)
    sport_obj = Sports.parse_obj(update_item_encoded)
    create_update_sports(sport_obj, sport_id)
    return update_item_encoded


@app.post("/sports/", response_model=model.Sports)
async def update_sport(sport: model.Sports):
    update_item_encoded = jsonable_encoder(sport)
    sport_obj = Sports.parse_obj(update_item_encoded)
    create_update_sports(sport_obj)
    return update_item_encoded

"""
Event API
"""


@app.get("/events/{event_id}", response_model=model.EventsIn)
async def read_events(event_id: int):
    return get_objects_by_id('events', event_id)


@app.get("/events/", response_model=List[model.EventsIn])
async def read_all_events():
    return get_all_objects('events')


@app.put("/events/{event_id}", response_model=model.Events)
async def update_events(event_id: int, item: model.Events):
    update_item_encoded = jsonable_encoder(item)
    event = model.Events.parse_obj(update_item_encoded)
    event = create_update_event(event, event_id)
    return event


@app.post("/events/", response_model=model.EventsIn)
async def create_events(item: model.Events):
    update_item_encoded = jsonable_encoder(item)
    event = model.Events.parse_obj(update_item_encoded)
    event = create_update_event(event)
    return event


"""
Selections API
"""

@app.get("/selections/{selection_id}", response_model=model.Selections)
async def read_selections(selection_id: int):
    return get_objects_by_id('selections', selection_id)


@app.get("/selections/", response_model=List[model.Selections])
async def read_all_selections():
    return get_all_objects('selections')


@app.put("/selections/{selection_id}", response_model=model.Selections)
async def update_selections(selection_id: int, item: model.Selections):
    update_item_encoded = jsonable_encoder(item)
    selection = model.Selections.parse_obj(update_item_encoded)
    selection = create_update_selection(selection, selection_id)
    return selection


@app.post("/selections/", response_model=model.Selections)
async def create_selections(item: model.Selections):
    update_item_encoded = jsonable_encoder(item)
    selection = model.Selections.parse_obj(update_item_encoded)
    selection = create_update_selection(selection)
    return selection



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)