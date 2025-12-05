SELECT
    $displaycolumns
FROM $table1
WHERE Cast("$column2" AS VARCHAR) NOT LIKE  '%'|| Cast("$column1" AS VARCHAR)||'%';