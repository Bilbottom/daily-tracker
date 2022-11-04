
DROP TABLE IF EXISTS tracker;
CREATE TABLE tracker(
    date_time DATETIME NOT NULL PRIMARY KEY UNIQUE,
    task TEXT NOT NULL,
    detail TEXT NOT NULL DEFAULT '',
    interval INTEGER NOT NULL
)
;
CREATE INDEX tracker_task
    ON tracker(task)
;


DROP TABLE IF EXISTS task_last_detail;
CREATE TABLE task_last_detail(
    task TEXT NOT NULL PRIMARY KEY UNIQUE REFERENCES tracker(task),
    detail TEXT NOT NULL,
    last_date_time DATETIME NOT NULL
)
;


DROP TRIGGER IF EXISTS set_tracker_latest_task;
CREATE TRIGGER set_tracker_latest_task
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
-- CREATE INDEX tracker_latest_tasks
--     ON task_last_detail(task, detail)
--     WHERE last_date_time >= DATETIME(MAX(last_date_time) OVER(), '-14 days')
-- ;


-- DROP VIEW IF EXISTS tracker_latest_task;
-- CREATE VIEW tracker_latest_task AS
--     SELECT
--         task,
--         detail,
--         last_date_time
--     FROM task_last_detail
--     WHERE last_date_time >= DATETIME('now', '-14 days')
-- ;
