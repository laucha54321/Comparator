SELECT
    "Sales Document",
    "Sales Office: Territory Code",
    "Customer_Group_2",
FROM joined_sap_sfdc
WHERE "Sales Office: Territory Code" != "Customer_Group_2";