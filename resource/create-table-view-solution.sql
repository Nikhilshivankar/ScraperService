-- View definition for joined product URL and client metadata
CREATE VIEW IF NOT EXISTS active_product_urls AS
SELECT
    p.id AS product_url_id,
    p.url,
    p.source_type,
    p.status,
    p.created_at AS url_created_at,
    c.id AS client_id,
    c.name AS client_name,
    c.active AS client_active
FROM product_urls p
JOIN clients c ON p.client_id = c.id
WHERE p.status = 1
  AND c.deleted_at IS NULL;

-- Job summary view for simplified reporting
CREATE VIEW IF NOT EXISTS job_status_summary AS
SELECT
    id AS job_id,
    submitted_by,
    submitted_at,
    status,
    jobtype,
    client_name,
    scrape_type,
    scheduled_at,
    done_at
FROM job_data;
