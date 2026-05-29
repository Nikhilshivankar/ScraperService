DROP TRIGGER IF EXISTS trg_job_data_id;
DROP TABLE IF EXISTS id_sequence;
DROP TABLE IF EXISTS job_data;
DROP TABLE IF EXISTS job;

CREATE TABLE id_sequence (
    id INTEGER NOT NULL
);
INSERT INTO id_sequence(id)
VALUES (99999999);

CREATE TABLE IF NOT EXISTS job_data (
    id INTEGER PRIMARY KEY,
    submitted_by TEXT NOT NULL,
    submitted_at DATETIME NOT NULL DEFAULT (CURRENT_TIMESTAMP),
    status TEXT NOT NULL DEFAULT 'New',
    jobtype TEXT NOT NULL DEFAULT 'Scraper',
    client_name TEXT,
    scrape_type TEXT,
    changed_by TEXT,
    changed_at DATETIME,
    scheduled_at DATETIME,
    done_at DATETIME
);

CREATE TRIGGER trg_job_data_id
AFTER INSERT ON job_data
FOR EACH ROW
BEGIN
    UPDATE job_data
    SET id = (SELECT id + 1 FROM id_sequence), 
    submitted_by = NEW.submitted_by, 
    submitted_at = NEW.submitted_at, 
    status = NEW.status, 
    jobtype = NEW.jobtype, 
    client_name = NEW.client_name, 
    scrape_type = NEW.scrape_type, 
    changed_by = NEW.changed_by, changed_at = NEW.changed_at, scheduled_at = NEW.scheduled_at, done_at = NEW.done_at

    WHERE rowid = NEW.rowid;
    UPDATE id_sequence
    SET id = (SELECT MAX(id) FROM job_data);
END;


CREATE TABLE IF NOT EXISTS clients (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    created_at DATETIME NOT NULL DEFAULT (CURRENT_TIMESTAMP),
    updated_at DATETIME NOT NULL DEFAULT (CURRENT_TIMESTAMP),
    deleted_at DATETIME,
    created_by TEXT,
    updated_by TEXT,
    deleted_by TEXT,
    active BOOLEAN NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS product_urls (
    id INTEGER PRIMARY KEY,
    url TEXT NOT NULL UNIQUE,
    source_type TEXT NOT NULL DEFAULT 'Sitemap',
    client_id INTEGER NOT NULL,
    created_at DATETIME NOT NULL DEFAULT (CURRENT_TIMESTAMP),
    status BOOLEAN NOT NULL DEFAULT 1,
    FOREIGN KEY (client_id) REFERENCES clients(id)
);

CREATE TABLE IF NOT EXISTS product_info (
    id INTEGER PRIMARY KEY,
    client_id INTEGER NOT NULL,
    name TEXT,
    image TEXT,
    price TEXT,
    updated_at DATETIME NOT NULL DEFAULT (CURRENT_TIMESTAMP)
);




