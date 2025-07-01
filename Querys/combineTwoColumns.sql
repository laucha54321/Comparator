SELECT
    *,
    CAST("$column1" AS VARCHAR) || ' ' || CAST("$column2" AS VARCHAR) AS newcolumn1
FROM joined_sap_sfdc;
