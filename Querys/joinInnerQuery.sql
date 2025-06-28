SELECT 
 $displaycolumns
FROM SAP_ORDERS AS sap
INNER JOIN SFDC_ORDERS AS sfdc
  ON sfdc."$sfdccolumn" = sap."$sapcolumn"
