SELECT *
FROM SAP_INVOICES AS sap
INNER JOIN SFDC_INVOICES AS sfdc
  ON sfdc."Billing Doc Number" = sap."Billing Document"
  AND sfdc."Invoice Item" = sap."Item"
