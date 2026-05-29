-- Fixed create table script for ScraperService schema
-- This file reflects the current SQLAlchemy models and corrected table definitions.

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
