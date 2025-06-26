SELECT 
  "Sales Document", 
  MAX("Cust. Code") AS Cust_Code, 
  MAX("Sales Document Type") AS Sales_Doc_Type, 
  MAX("Pay Term") AS Pay_Term, 
  MAX("Customer Group 2") AS Customer_Group_2,
  MAX("Tax Number 1 (CNPJ No.)") AS CNPJ,
  MAX("Billing Date") AS Billing_Date, 
  SUM("ZCP1 Condition Type Value") AS Total_ZCP1,
  SUM("Rejected Qty") AS Rejected_Qty,
  SUM(("Net Price" * "Order Quantity") - ("Rejected Qty" * "Net Price")) AS Total_Value
FROM SAP_ORDERS_LINEITEMS
GROUP BY "Sales Document"
ORDER BY "Sales Document";
