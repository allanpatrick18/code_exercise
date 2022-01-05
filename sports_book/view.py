import logging
import pytz
from psycopg2 import sql
from sql_queries import *
from typing import Optional
from connection import return_db_connection
from datetime import datetime, timezone
from model import Sports, EventsIn, Events, Selections

cur = return_db_connection()


class FilterMissingError(Exception):
    """Custom error that is raised param table doesn't
      is missing."""
    message: str = "The filter doesn't exits"


def execute_query_object(sql_stmt, values=None):
    """This function execute the query statements"""
    cur = return_db_connection()
    if values:
        cur.execute(sql_stmt, values)
    else:
        cur.execute(sql_stmt)
    data_store = []
    for r in cur.fetchall():
        data_store.append(dict(r))
    cur.close()
    return data_store


def execute_regex_sql(table_name: str, expression: str) -> dict():
    data_store = []
    cur = return_db_connection()
    with cur as cursor:
        stmt = sql.SQL("""
           SELECT * 
           FROM {table_name} 
           WHERE {field} ~ {regex}
        """).format(
            table_name=sql.Identifier(table_name),
            field=sql.Identifier('name'),
            regex=sql.Literal(expression)
        )
        cursor.execute(stmt)
        result = cursor.fetchall()

    for r in result:
        data_store.append(dict(r))
    return result


def generate_insert_sql(model):
    """
    This function will generate insert sql
    statement based in the give model
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
    event.scheduled_start = event.scheduled_start.replace(tzinfo=timezone.utc)
    if id == None:
        statement, values = generate_insert_sql(event)
    else:
        statement, values = generate_update_sql(event, id)
    cur.execute(statement, values)
    res_obj = dict(cur.fetchone())
    return res_obj


def create_update_selection(selection: Selections, id=None):
    if id == None:
        statement, values = generate_insert_sql(selection)
    else:
        statement, values = generate_update_sql(selection, id)
    cur.execute(statement, values)
    res_obj = dict(cur.fetchone())
    return res_obj


def get_all_objects(table_name: str) -> Optional[list]:
    stm = select_all.format(table_name=table_name)
    res = execute_query_object(stm)
    return res


def get_objects_by_id(table_name: str, item_id: int) -> list:
    stm = select_by_id.format(table_name=table_name, id=item_id)
    res = execute_query_object(stm)
    if res:
        return res[0]
    return res


def get_regex_by_table(table: str, params: dict) -> dict:
    result_dict = dict()
    stm = None
    filters = [f for f in list(params.keys())]
    and_clause = []
    try:
        if 'regex' in filters:
            and_clause.append("%s  ~ '%s'" % ('name', params['regex']))

        if 'start_dt' and 'end_dt' in filters:
            start_dt = datetime.fromisoformat(params['start_dt'])
            end_dt = datetime.fromisoformat(params['start_dt'])
            start_dt_utc = start_dt.astimezone(pytz.utc)
            end_dt_utc = end_dt.astimezone(pytz.utc)
            and_clause.append("%s BETWEEN '%s' AND '%s'" % ('scheduled_start', start_dt_utc, end_dt_utc))

        and_clause_str = ' AND '.join(and_clause)
        if 'threshold' in filters:
            if table not in map_queries:
                raise FilterMissingError

            stm = map_queries[table]['threshold'].format(threshold=params['threshold'])
            stm = f'{stm} WHERE ' + and_clause_str
        else:
            sql_query = f'SELECT * FROM {table} WHERE ' + and_clause_str
            stm = sql_query
    except FilterMissingError as e:
        logging.info(msg=e.message)

    if stm:
        res = execute_query_object(stm)
        result_dict[table] = res
    return result_dict


def get_regex(table: str, params: dict) -> dict:
    result_dict = dict()
    and_clause = []
    for k, v in params.items():
        and_clause.append("%s  ~ " % (k) +" %s")

    and_clause_str = ' AND '.join(and_clause)
    sql_query = f'SELECT * FROM {table} WHERE ' + and_clause_str
    res = execute_query_object(sql_query, tuple(params.values()),)
    result_dict[table] = res

    return result_dict