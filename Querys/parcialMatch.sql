SELECT
    $displaycolumns
FROM joined_sap_sfdc
WHERE Cast("$column2" AS VARCHAR) NOT LIKE  '%'|| Cast("$column1" AS VARCHAR)||'%';