SELECT *
FROM SAP_ORDERS AS sap
INNER JOIN SFDC_ORDERS AS sfdc
  ON sfdc."SAP Order Number"  = sap."Sales Document" 
