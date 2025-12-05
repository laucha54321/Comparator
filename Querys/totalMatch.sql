SELECT
    $displaycolumns
FROM $table1
WHERE Cast("$column2" as VARCHAR) != Cast("$column1"as VARCHAR);