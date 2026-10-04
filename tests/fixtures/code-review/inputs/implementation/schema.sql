-- Supplied synthetic prior schema only; NOT EXECUTED.
CREATE TABLE score_records (
 id BIGINT UNSIGNED PRIMARY KEY COMMENT 'Record identity',
 school_id BIGINT UNSIGNED NOT NULL COMMENT 'School identity',
 year INT NOT NULL COMMENT 'Academic year',
 student_id BIGINT UNSIGNED NOT NULL COMMENT 'Student identity',
 score DECIMAL(6,2) NULL COMMENT 'Score',
 threshold DECIMAL(6,2) NULL COMMENT 'Threshold',
 offset INT NULL COMMENT 'Existing offset'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='Score records';
