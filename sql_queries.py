sport_table_drop = "DROP TABLE IF EXISTS sports"
events_table_drop = "DROP TABLE IF EXISTS events"
selection_table_drop = "DROP TABLE IF EXISTS selections"


sports_table_create = """
CREATE TABLE IF NOT EXISTS sports
( id SERIAL PRIMARY KEY,
name VARCHAR (255) ,
slug VARCHAR (255),
active boolean
);
"""

event_table_create = """
CREATE TABLE IF NOT EXISTS events
(
id SERIAL PRIMARY KEY,
name VARCHAR (255),
slug VARCHAR (255),
sport_id int constraint event_sports_id_fk references sports,
active boolean,
status VARCHAR(25),
scheduled_start timestamp without time zone,
actual_start timestamp
);"""

selection_table_create = """
CREATE TABLE IF NOT EXISTS selections
(
id SERIAL PRIMARY KEY,
slug VARCHAR(255),
name VARCHAR(255),
active BOOLEAN,
outcome VARCHAR(25),
price DECIMAL,
event_id int 
constraint selection_event_id_fk
        references event
);"""

insert_table_sports = """
insert into sports (name, slug, active)
values ('{name}', '{slug}', '{active}');
"""

update_table_sports = """
UPDATE sports
SET name = '{name}',
    slug= '{slug}',
    active = '{active}'
WHERE id = {id};
"""

select_all = """SELECT * FROM {table_name}"""

select_by_id = """SELECT * FROM public.{table_name} WHERE id = {id}"""

create_table_queries = [sports_table_create, event_table_create, selection_table_create]
drop_table_queries = [sport_table_drop, events_table_drop, selection_table_drop]