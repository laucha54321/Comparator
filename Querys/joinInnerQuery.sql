SELECT 
 $displaycolumns
FROM SAP_ORDERS AS sap
INNER JOIN SFDC_ORDERS AS sfdc
  ON sfdc."$column2" = sap."$column1"
