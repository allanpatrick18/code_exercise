from psycopg2 import sql
from sql_queries import *
from connection import return_db_connection
from model import Sport, EventIn, Event


def execute_query_object(sql_stmt):
    """This function execute the query statements"""
    cur, conn = return_db_connection()
    cur.execute(sql_stmt)
    data_store = []
    for r in cur.fetchall():
        print(dict(r))
        data_store.append(dict(r))
    cur.close()
    return data_store


def create_update_sports(sport: Sport, id=None):
    cur, conn = return_db_connection()
    if id == None:
        names = tuple(sport.schema()['properties'].keys())
        string = tuple(['%s' for i in range(len(names))])
        statement = insert_table_sports.format('sports', names, string).replace("'", "")
        values = tuple(sport.dict().values())
        cur.execute(statement, values)
    else:
        sport = sport.dict()
        stm = update_table_sports.format(id=id,
                                         name=sport['name'],
                                         slug=sport['slug'],
                                         active=sport['active'])

        cur.execute(stm)
    res_obj = dict(cur.fetchone())
    return res_obj


def create_update_event(event: EventIn, id=None):
    cur, conn = return_db_connection()
    if id == None:
        names = tuple(EventIn.schema()['properties'].keys())
        string = tuple(['%s' for i in range(len(names))])
        statement = insert_table_sports.format('events', names, string).replace("'", "")
        event = EventIn.parse_obj(event.dict())
        values = tuple(event.dict().values())
        print(statement, values)
        cur.execute(statement, values)
    else:
        stm = update_table_sports.format(id=id,
                                         name=event['name'],
                                         slug=event['slug'],
                                         active=event['active'])

        cur.execute(stm)
    res_obj = dict(cur.fetchone())
    return res_obj

def get_all_objects(table_name):
    stm = select_all.format(table_name=table_name)
    res = execute_query_object(stm)
    return res


def get_objects_by_id(table_name, item_id):
    stm = select_by_id.format(table_name=table_name, id=item_id)
    print(stm)
    res = execute_query_object(stm)
    if res:
        return res[0]
    return res