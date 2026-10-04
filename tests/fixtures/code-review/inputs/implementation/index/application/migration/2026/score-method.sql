ALTER TABLE score_records ADD COLUMN method TINYINT NOT NULL;
UPDATE score_records SET offset = 0;
ALTER TABLE score_records ADD UNIQUE KEY uk_score_records_01 (school_id, year, student_id);
ALTER TABLE score_records ADD CONSTRAINT record_student FOREIGN KEY (student_id) REFERENCES students(id);
