
SELECT 
  "Sales Document", "Cons. Code", "Shipping Address"
FROM joined_sap_sfdc
WHERE CAST("Shipping Address" AS VARCHAR) NOT LIKE '%' || CAST("Cons. Code" AS VARCHAR) || '%';
