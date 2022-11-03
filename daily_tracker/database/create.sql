
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
