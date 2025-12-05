SELECT *
FROM SAP_ORDERS_LINEITEMS AS sap
FULL OUTER JOIN SFDC_ORDERS AS sfdc
  ON sfdc."SAP Order Number" = sap."Sales Document"
  AND sfdc."Item Number" = sap."Sales Document Item"
WHERE sfdc."SAP Order Number" IS NULL 
   OR sap."Sales Document" IS NULL
   OR sfdc."Item Number" IS NULL 
   OR sap."Sales Document Item" IS NULL;

