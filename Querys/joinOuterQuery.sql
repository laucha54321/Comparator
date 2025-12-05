SELECT 
  $displaycolumns
FROM "$table1" AS "$table1"
FULL OUTER JOIN "$table2" AS "$table2"
  ON "$table1"."$column1" = "$table2"."$column2"
WHERE "$table1"."$column1" IS NULL OR "$table2"."$column2" IS NULL;
