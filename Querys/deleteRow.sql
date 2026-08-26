-- deleteRow.sql
-- DuckDB query that deletes rows and returns them
DELETE FROM "$table1"
WHERE "$table1"."$column1" IN ($table2)
RETURNING *;