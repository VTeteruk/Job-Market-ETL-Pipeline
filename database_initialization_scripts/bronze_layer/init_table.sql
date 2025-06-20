/*
=====================================================
Job Market ETL Pipeline - Bronze Layer Table Setup
=====================================================
Purpose: Creates the bronze.jobs table for storing raw job data from multiple sources
Layer: Bronze (raw data ingestion layer)
Sources: Job platforms
=====================================================
*/

DROP TABLE IF EXISTS bronze.jobs;

CREATE TABLE bronze.jobs (
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
	salary VARCHAR(50),
	posted_date DATE,
	applicant_count INT,
	view_count INT,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);