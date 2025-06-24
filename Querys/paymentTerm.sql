SELECT
    "Sales Document",
    "Pay_Term",
    "Payment Term: Payment Term Code",
FROM joined_sap_sfdc
WHERE "Payment Term: Payment Term Code" != "Pay_Term";
