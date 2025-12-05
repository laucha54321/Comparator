SELECT 
  "Sales Document", 
  MAX("Cust. Code") AS "Cust. Code", 
  MAX("Cons. Code") AS "Cons. Code",
  MAX("Pay Term") AS "Pay Term",
  MAX("Tax Number 1 (CNPJ No.)") AS "Tax Number 1 (CNPJ No.)",
  MAX("Customer Group 2") AS "Customer Group 2",
  MAX("Commission Agent Desc.") AS "Commission Agent Desc.",
  MAX("Billing Date") AS "Billing Date", 
  SUM("Rejected Qty") AS "Rejected Qty",
  SUM(("Net Price" * "Order Quantity") - ("Rejected Qty" * "Net Price")) AS "Total Value"
FROM SAP_ORDERS_LINEITEMS
GROUP BY "Sales Document"
ORDER BY "Sales Document";
