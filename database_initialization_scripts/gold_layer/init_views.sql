/*
===============================
THE MOST HIRING LOCATIONS VIEW
===============================
This view analyzes job postings by location, showing:
- Number of jobs per location
- Average monthly salary in EUR (normalized from different periods)
*/

CREATE OR REPLACE VIEW gold.most_hiring_location_view AS
SELECT
    location,
    COUNT(*) AS jobs_count,
    ROUND(
        AVG(
            CASE
                WHEN salary_period = 'month' AND salary_currency = 'EUR'
                    THEN salary_amount

                WHEN salary_period = 'year' AND salary_currency = 'EUR'
                    THEN ROUND(salary_amount / 12.0, 2)

                WHEN salary_period = 'hour' AND salary_currency = 'EUR'
                    THEN ROUND(salary_amount * 160, 2)  -- Assuming 160 hours/month (40h/week * 4 weeks)

                ELSE NULL
            END
        ), 2
    ) AS avg_monthly_salary_eur

FROM silver.jobs
WHERE location IS NOT NULL
    AND location != 'n/a'
    AND location != ''  -- Exclude empty strings as well

GROUP BY location
ORDER BY jobs_count DESC;


-- ====================
-- MARKET OVERVIEW VIEW
-- ====================
CREATE OR REPLACE VIEW gold.market_overview AS
SELECT
    COUNT(*) as total_jobs,
    COUNT(DISTINCT company) as unique_companies,
    COUNT(DISTINCT location) as unique_locations,
    COUNT(DISTINCT title) as unique_job_titles,
    ROUND(AVG(CASE
        WHEN salary_period = 'month' AND salary_currency = 'EUR' THEN salary_amount
        WHEN salary_period = 'year' AND salary_currency = 'EUR' THEN ROUND(salary_amount / 12.0)
        WHEN salary_period = 'hour' AND salary_currency = 'EUR' THEN ROUND(salary_amount * 160)
        ELSE NULL
    END)) as avg_monthly_salary_eur,
    ROUND(AVG(applicant_count)) as avg_applicants_per_job,
    ROUND(AVG(view_count)) as avg_views_per_job,
    DATE(MAX(posted_date)) as latest_posting_date,
    DATE(MIN(posted_date)) as earliest_posting_date
FROM silver.jobs;
