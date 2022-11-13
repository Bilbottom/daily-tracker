
/*
    + main.tracker +
    The core table in this application that holds all historic data.
*/
DROP TABLE IF EXISTS tracker;
CREATE TABLE tracker(
    date_time DATETIME NOT NULL PRIMARY KEY UNIQUE,
    task TEXT NOT NULL,
    detail TEXT NOT NULL DEFAULT '',
    interval INTEGER NOT NULL
);
CREATE INDEX tracker_task
    ON tracker(task)
;


/*
    + main.task_last_detail +
    The latest detail per task. Used for automatically filling the detail text
    box for each task. Updates on inserts and updates of the main.tracker table.
*/
DROP TABLE IF EXISTS task_last_detail;
CREATE TABLE task_last_detail(
    task TEXT NOT NULL PRIMARY KEY UNIQUE REFERENCES tracker(task),
    detail TEXT NOT NULL,
    last_date_time DATETIME NOT NULL
);
-- CREATE INDEX tracker_latest_tasks
--     ON task_last_detail(task, detail)
--     WHERE last_date_time >= DATETIME(MAX(last_date_time) OVER(), '-14 days')
-- ;


DROP TRIGGER IF EXISTS set_tracker_latest_task_on_insert;
CREATE TRIGGER set_tracker_latest_task_on_insert
    BEFORE INSERT ON tracker
BEGIN
    INSERT INTO task_last_detail
    VALUES (NEW.task, NEW.detail, NEW.date_time)
    ON CONFLICT(task) DO UPDATE
    SET detail = NEW.detail,
        last_date_time = NEW.date_time
    ;
END
;

DROP TRIGGER IF EXISTS set_tracker_latest_task_on_update;
CREATE TRIGGER set_tracker_latest_task_on_update
    BEFORE UPDATE ON tracker
BEGIN
    INSERT INTO task_last_detail
    VALUES (NEW.task, NEW.detail, NEW.date_time)
    ON CONFLICT(task) DO UPDATE
    SET detail = NEW.detail,
        last_date_time = NEW.date_time
    ;
END
;


/*
    + main.default_tasks +
    The default tasks used to populate the task input box drop-down. This should
    be configurable outside of this module.
*/
DROP TABLE IF EXISTS default_tasks;
CREATE TABLE default_tasks(
    task TEXT NOT NULL UNIQUE
);
INSERT INTO default_tasks
VALUES
    ('Lunch Break'),
    ('Meetings'),
    ('Housekeeping'),
    ('Adhoc Chat'),
    ('Adhoc Task'),
    ('Documentation'),
    ('Personal Development'),
    ('Unable to Work')
;
INSERT INTO task_last_detail(task, detail, last_date_time)
    SELECT
        task,
        '',
        ''
FROM default_tasks
;


/*
    + main.tracker_latest_task +
    The latest detail per task over the last 14 days.

    ! The last "14 days" should be configurable, so this shouldn't be done in a
    ! view. Also, this view doesn't really add any value.
*/
/*
DROP VIEW IF EXISTS tracker_latest_task;
CREATE VIEW tracker_latest_task AS
    SELECT
        task,
        detail,
        last_date_time
    FROM task_last_detail
    WHERE last_date_time >= DATETIME('now', '-14 days')
       OR last_date_time = ''
;
*/
