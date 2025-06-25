/*
=====================================================
Job Market ETL Pipeline - Silver Layer Table Setup
=====================================================
Purpose : Creates the silver.jobs table for storing cleaned and normalized job listings
Layer   : Silver (cleaned, structured data ready for analysis)
Sources : Processed outputs from the bronze layer
Notes   : Salary data is split into amount, currency, and period for structured querying.
=====================================================
*/

DROP TABLE IF EXISTS silver.jobs;

CREATE TABLE silver.jobs (
	job_id BIGINT PRIMARY KEY,
	url VARCHAR(255) NOT NULL,
	source VARCHAR(255) NOT NULL,
	title VARCHAR(255),
	company VARCHAR(255),
	location VARCHAR(255),
	job_type VARCHAR(255),
	workplace_type VARCHAR(255),
	experience_level VARCHAR(255),
	description TEXT,
	salary_amount INT,
	salary_currency VARCHAR(50),
	salary_period VARCHAR(50),
	posted_date DATE,
	applicant_count INT,
	view_count INT,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);