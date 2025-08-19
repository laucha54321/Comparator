SELECT *
FROM SAP_ORDERS_LINEITEMS AS sap
INNER JOIN SFDC_ORDERS AS sfdc
  ON sfdc."SAP Order Number" = sap."Sales Document"
  AND sfdc."Item Number" = sap."Sales Document Item"
