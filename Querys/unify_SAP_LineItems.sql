SELECT 
  "Sales Document", 
  MAX("Cust. Code") AS Cust_Code, 
  MAX("Sales Document Type") AS Sales_Doc_Type, 
  MAX("Pay Term") AS Pay_Term, 
  MAX("Tax Number 1 (CNPJ No.)") AS CNPJ,
  MAX("Billing Date") AS Billing_Date, 
  SUM("ZCP1 Condition Type Value") AS Total_ZCP1
FROM SAP_ORDERS_LINEITEMS
GROUP BY "Sales Document"
ORDER BY "Sales Document";
