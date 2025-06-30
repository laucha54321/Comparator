SELECT *
FROM SAP_INVOICES AS sap
INNER JOIN SFDC_INVOICES AS sfdc
  ON sfdc."E-Invoice No." = sap."Billing Document"
  AND sfdc."Invoice Item" = sap."Line Number"
