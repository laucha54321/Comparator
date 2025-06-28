SELECT
    "Sales Document",
    "Cust Code",
    "Order Amount",
    "Importe Neto",
    "Total ZCP1",
    "Total Value",
    ABS("Importe Neto" - "Total Value") AS Difference_ImporteNeto_TotalValue,
FROM joined_sap_sfdc
WHERE (ABS("Importe Neto" - "Total Value") > 10);

-- este query toma el valor Total_Value que calculo como p * q en unify sap line items