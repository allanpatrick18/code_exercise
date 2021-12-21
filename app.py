import uvicorn
from typing import Optional
from typing import List
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from datetime import datetime
from urllib.parse import unquote

# from create_tables import main
# main()

import model
from sports_book.view import *
import logging


#APScheduler Related Libraries
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

app = FastAPI()

Schedule = None
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.get("/")
async def read_main():
    return {"msg": "Sever Up!"}


@app.get("/regex/{expression}", response_model=Optional[dict])
async def read_regex(expression: str):
    expression = unquote(expression)
    print(expression)
    return get_regex(expression)


@app.on_event("startup")
async def load_schedule_or_create_blank():
    """
    Instatialise the Schedule Object as a Global Param and also load existing Schedules from Postgres
    This allows for persistent schedules across server restarts.
    """
    global Schedule
    try:
        jobstores = {
            'default': SQLAlchemyJobStore(url='postgresql://postgres:postgres@localhost:5432/sports_book')
        }
        Schedule = AsyncIOScheduler(jobstores=jobstores)
        Schedule.start()
        logger.info("Created Schedule Object")
    except:
        logger.error("Unable to Create Schedule Object")


@app.on_event("shutdown")
async def pickle_schedule():
    """
    An Attempt at Shutting down the schedule to avoid orphan jobs
    """
    global Schedule
    Schedule.shutdown()
    logger.info("Disabled Schedule")

"""
Sports API
"""


@app.get("/sports/{sport_id}", response_model=model.Sports)
async def read_sport(sport_id: int):
    return get_objects_by_id('sports', sport_id)


@app.get("/sports/", response_model=List[model.Sports])
async def read_all_sports():
    return get_all_objects('sports')


@app.get("/sports/", response_model=List[model.Sports])
async def read_all_sports(q: Optional[str] = None):
    if q:
        print(q)
    return get_all_objects('sports')


@app.put("/sports/{sport_id}", response_model=model.Sports)
async def update_sport(sport_id: str, item: model.Sports):
    update_item_encoded = jsonable_encoder(item)
    sport_obj = Sports.parse_obj(update_item_encoded)
    result = create_update_sports(sport_obj, sport_id)
    return result


@app.post("/sports/", response_model=model.Sports)
async def update_sport(sport: model.Sports):
    update_item_encoded = jsonable_encoder(sport)
    sport_obj = Sports.parse_obj(update_item_encoded)
    result = create_update_sports(sport_obj)
    return result


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


def check_schedule_event(event):
    """ This event"""
    end_date = event['scheduled_start']
    time_to_expiry = (end_date - datetime.now()).days
    print(time_to_expiry)


@app.put("/events/{event_id}", response_model=model.Events)
async def update_events(event_id: int, item: model.Events):
    update_item_encoded = jsonable_encoder(item)
    event = model.Events.parse_obj(update_item_encoded)
    event = create_update_event(event, event_id)
    # end_date = event['scheduled_start']
    # time_to_expiry = (end_date - datetime.now()).days
    # schedule_check = Schedule.add_job(check_schedule_event, 'interval', seconds=time_to_expiry, id=event['id'],
    #                                   args=[event])
    # print(schedule_check)
    return event


@app.post("/events/", response_model=model.EventsIn)
async def create_events(item: model.Events):
    update_item_encoded = jsonable_encoder(item)
    event = model.Events.parse_obj(update_item_encoded)
    event = create_update_event(event)
    end_date = event['scheduled_start']
    index_job = str(event['id']) + '_' + event['name']
    # time_to_expiry = (end_date - datetime.now()).days
    # schedule_check = Schedule.add_job(check_schedule_event, 'interval', seconds=abs(time_to_expiry),
    #                                   id=index_job, args=[event])
    # print(schedule_check)
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