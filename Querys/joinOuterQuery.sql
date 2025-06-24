SELECT *
FROM SAP_ORDERS AS sap
FULL OUTER JOIN SFDC_ORDERS AS sfdc
  ON sfdc."SAP Order Number" = sap."Sales Document"
WHERE sfdc."SAP Order Number" IS NULL OR sap."Sales Document" IS NULL;
