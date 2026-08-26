SELECT *
FROM SAP_INVOICES AS sap
FULL OUTER JOIN SFDC_INVOICES AS sfdc
  ON sfdc."Billing Doc Number" = sap."Billing Document"
  AND sfdc."Invoice Item" = sap."Line Number"
WHERE sfdc."Billing Doc Number" IS NULL 
   OR sap."Billing Document" IS NULL
   OR sfdc."Invoice Item" IS NULL 
   OR sap."Line Number" IS NULL;
