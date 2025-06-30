SELECT 
  "Sales Document", 
  MAX("Cust. Code") AS "Cust. Code", 
  MAX("Sales Document Type") AS "Sales Document Type", 
  MAX("Pay Term") AS "Pay Term", 
  MAX("Customer Group 2") AS "Customer Group 2",
  MAX("Tax Number 1 (CNPJ No.)") AS "Tax Number 1 (CNPJ No.)",
  MAX("Billing Date") AS "Billing Date", 
  SUM("ZCP1 Condition Type Value") AS "ZCP1 Condition Type Value",
  SUM("Rejected Qty") AS "Rejected Qty",
  SUM(("Net Price" * "Order Quantity") - ("Rejected Qty" * "Net Price")) AS "Total Value"
FROM SAP_ORDERS_LINEITEMS
GROUP BY "Sales Document"
ORDER BY "Sales Document";
