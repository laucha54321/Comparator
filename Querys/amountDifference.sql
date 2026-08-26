-- Parameterized version of Net Value Mismatch query
SELECT
    ${displaycolumns}
FROM ${table1}
WHERE (ABS("${column1}") - ABS("${column2}") > ${threshold});