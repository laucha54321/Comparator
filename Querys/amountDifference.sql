SELECT
    "Sales Document",
    "Cust_Code",
    "Order Amount",
    "Total_ZCP1",
    ABS("Order Amount" - "Total_ZCP1") AS Difference,
FROM joined_sap_sfdc
WHERE ABS("Order Amount" - "Total_ZCP1") > 100;
