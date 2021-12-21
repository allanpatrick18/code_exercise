from psycopg2 import sql
from sql_queries import *
from typing import Optional
from connection import return_db_connection
from model import Sports, EventsIn, Events, Selections

cur = return_db_connection()

def execute_query_object(sql_stmt):
    """This function execute the query statements"""
    cur = return_db_connection()
    cur.execute(sql_stmt)
    data_store = []
    for r in cur.fetchall():
        print(dict(r))
        data_store.append(dict(r))
    cur.close()
    return data_store


def generate_insert_sql(model):
    """
    This function will generate insert sql
    statament based in the give model
    """
    names = list(model.schema()['properties'].keys())
    if 'id' in names:
        names.remove('id')
    fields = tuple(names)
    string = tuple(['%s' for i in range(len(names))])
    statement = insert_table.format(model.schema()['title'].lower(), fields, string).replace("'", "")
    values = tuple(model.dict(exclude={'id'}).values())
    return statement, values


def generate_update_sql(model, id: int):
    """ This function will generate model"""
    names = list(model.schema()['properties'].keys())
    if 'id' in names:
        names.remove('id')
    string = ', '.join(names)
    statement = update_table.format(model.schema()['title'].lower(), string, id).replace("'", "")
    values = (tuple(model.dict(exclude={'id'}).values()),)
    return statement, values


def create_update_sports(sport: Sports, id=None):
    if id == None:
        statement, values = generate_insert_sql(sport)
    else:
        statement, values = generate_update_sql(sport, id)
    cur.execute(statement, values)
    res_obj = dict(cur.fetchone())
    return res_obj


def create_update_event(event: EventsIn, id=None):
    if id == None:
        statement, values = generate_insert_sql(event)
    else:
        statement, values = generate_update_sql(event, id)
    cur.execute(statement, values)
    res_obj = dict(cur.fetchone())
    return res_obj


def create_update_selection(event: Selections, id=None):
    if id == None:
        statement, values = generate_insert_sql(event)
    else:
        statement, values = generate_update_sql(event, id)
    cur.execute(statement, values)
    res_obj = dict(cur.fetchone())
    return res_obj


def get_all_objects(table_name: str) -> Optional[list]:
    stm = select_all.format(table_name=table_name)
    res = execute_query_object(stm)
    return res


def get_objects_by_id(table_name: str, item_id: int) -> list:
    stm = select_by_id.format(table_name=table_name, id=item_id)
    print(stm)
    res = execute_query_object(stm)
    if res:
        return res[0]
    return res


def get_regex(expression: str) -> dict:
    tables = ['sports', 'events', 'selections']
    result_dict = dict()
    for table in tables:
        stm = select_by_regex.format(table_name=table, expression=expression)
        res = execute_query_object(stm)
        result_dict[table] = res

    return result_dict