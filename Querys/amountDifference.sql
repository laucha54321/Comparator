SELECT
    "Sales Document",
    "Cust_Code",
    "Order Amount"AS SFDC_Order_Amount,
    "Importe Neto" AS SFDC_Importe_Neto,
    "Total_ZCP1" AS SAP_Total_ZCP1,
    "Total_Value"AS SAP_Total_Value,
    ABS("Importe Neto" - "Total_Value") AS Difference_ImporteNeto_TotalValue,
FROM joined_sap_sfdc
WHERE (ABS("Importe Neto" - "Total_Value") > 10);

-- este query toma el valor Total_Value que calculo como p * q en unify sap line items