SELECT
    "Sales Document",
    "Sales_Doc_Type",
    "Order Type"
FROM joined_sap_sfdc
WHERE "Order Type" NOT LIKE '%' || "Sales_Doc_Type" || '%';