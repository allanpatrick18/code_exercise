sport_table_drop = "DROP TABLE IF EXISTS sports"
events_table_drop = "DROP TABLE IF EXISTS events"
selection_table_drop = "DROP TABLE IF EXISTS selections"


sports_table_create = """
CREATE TABLE IF NOT EXISTS sports
( id SERIAL PRIMARY KEY,
name VARCHAR (255) ,
slug VARCHAR (255),
active boolean NOT NULL
);
"""

event_table_create = """
CREATE TABLE IF NOT EXISTS events
(
id SERIAL PRIMARY KEY,
name VARCHAR (255),
slug VARCHAR (255),
type VARCHAR(25),
sport_id int constraint event_sports_id_fk references sports,
status VARCHAR(25),
active BOOLEAN NOT NULL,
scheduled_start timestamp without time zone,
actual_start timestamp without time zone
);"""

selection_table_create = """
CREATE TABLE IF NOT EXISTS selections
(
id SERIAL PRIMARY KEY,
slug VARCHAR(255),
name VARCHAR(255),
active BOOLEAN NOT NULL,
outcome VARCHAR(25),
price DECIMAL,
event_id INT 
constraint selection_event_id_fk
        references events
);"""

insert_table = """
insert into {} {}
values {} RETURNING *;
"""

update_table = """
UPDATE {} SET ({}) = %s WHERE id = {}
RETURNING *;
"""

create_procedures = """
CREATE OR REPLACE FUNCTION changes_status()
  RETURNS TRIGGER
  LANGUAGE PLPGSQL
  AS
$$
BEGIN
IF NEW.status = 'Started' AND OLD.status !='Started' THEN
    UPDATE events
    SET  actual_start = CURRENT_TIMESTAMP
    WHERE NEW.id = events.id;
END IF;

RETURN NEW;
END;
$$;
"""

create_triggers = """
CREATE TRIGGER last_name_changes_after
AFTER UPDATE
ON events
FOR EACH ROW
EXECUTE PROCEDURE changes_status();
"""

select_all = """SELECT * FROM {table_name};"""

select_by_id = """SELECT * FROM public.{table_name} WHERE id = {id};"""

select_by_regex = """ SELECT * FROM {table_name} WHERE {field} ~ %s """

select_sport_by_threshold = """ 
SELECT * FROM
sports
INNER JOIN(
SELECT sport_id, count(*) as final FROM sports as s
INNER JOIN events e on s.id = e.sport_id
WHERE  e.active= TRUE
GROUP BY sport_id
HAVING count(*) > {threshold}
ORDER BY final DESC) as res
ON res.sport_id = id"""


select_event_by_threshold = """ 
SELECT * FROM
events
INNER JOIN(
SELECT event_id, count(*) as actives
FROM events as s
INNER JOIN selections s2 on s.id = s2.event_id
WHERE  s2.active= TRUE
GROUP BY event_id
HAVING count(*) > {threshold}
ORDER BY actives DESC) as res
ON res.event_id = id"""




map_queries = {'sports':  {'regex': select_by_regex,
                          'threshold': select_sport_by_threshold},
            'events':  {'regex': select_by_regex,
                       'threshold': select_event_by_threshold}

}

create_table_queries = [sports_table_create, event_table_create, selection_table_create, create_procedures,
                        create_triggers]
# drop_table_queries = [sport_table_drop, events_table_drop, selection_table_drop]

drop_table_queries = []