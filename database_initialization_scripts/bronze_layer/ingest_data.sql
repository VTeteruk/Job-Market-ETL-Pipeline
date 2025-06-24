COPY bronze.jobs (
    job_id, url, source, title, company, location, job_type,
    workplace_type, experience_level, description, salary,
    posted_date, applicant_count, view_count
)
FROM '/var/lib/postgresql/csv_files/<file_name>'
WITH (
    FORMAT csv,
    HEADER true,
    DELIMITER ',',
    QUOTE '"',
    ESCAPE '"'
);