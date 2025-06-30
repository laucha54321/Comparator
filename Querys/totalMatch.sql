SELECT
    $displaycolumns
FROM joined_sap_sfdc
WHERE "$sfdccolumn" != "$sapcolumn";