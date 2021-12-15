from sql_queries import *
from connection import return_db_connection
from model import Sport



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
    if id is None:
        stm = insert_table_sports.format(name=sport['name'],
                                         slug=sport['slug'],
                                         active=sport['active'])
    else:
        stm = update_table_sports.format(id=id,
                                         name=sport['name'],
                                         slug=sport['slug'],
                                         active=sport['active'])

    print(stm)
    cur.execute(stm)
    return True


def get_all_objects(table_name):
    stm = select_all.format(table_name=table_name)
    print(stm)
    res = execute_query_object(stm)
    return res


def get_objects_by_id(table_name, item_id):
    stm = select_by_id.format(table_name=table_name, id=item_id)
    res = execute_query_object(stm)
    return res[0]