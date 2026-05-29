-- Table creation template for SQLite schema files.
-- Replace <table_name> and <column definitions> with your own values.

CREATE TABLE IF NOT EXISTS <table_name> (
    id INTEGER PRIMARY KEY,
    <column_name> <data_type> [NOT NULL] [UNIQUE] [DEFAULT <default_value>],
    -- Use TEXT for string values, DATETIME for timestamps, BOOLEAN for boolean values.
    -- Add foreign keys as needed:
    -- FOREIGN KEY (<column_name>) REFERENCES other_table(id)
);

-- Example:
CREATE TABLE IF NOT EXISTS clients (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    created_at DATETIME NOT NULL DEFAULT (CURRENT_TIMESTAMP),
    updated_at DATETIME NOT NULL DEFAULT (CURRENT_TIMESTAMP),
    deleted_at DATETIME,
    active BOOLEAN NOT NULL DEFAULT 1
);
