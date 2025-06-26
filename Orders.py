import pandas as pd
import duckdb
import os 


### Save to excel function ####
def save_to_excel(df, sheet_name):
    file_path = "result.xlsx"
    if not os.path.exists(file_path):
        with pd.ExcelWriter(file_path, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name=sheet_name)
    else:
        with pd.ExcelWriter(file_path, mode='a', engine="openpyxl", if_sheet_exists='replace') as writer:
            df.to_excel(writer, index=False, sheet_name=sheet_name)

## Read Files#########################################################
sap_df = pd.read_excel("./Database/Orders/SAP - ZSD18A_ARG/Orders.xlsx", engine="openpyxl")
sfdc_df = pd.read_excel("./Database/Orders/SFDC - Access - Integrity Order Report/Access - Integrity Order Report-2025-06-26-09-20-03.xlsx", sheet_name="Access - Integrity Order Report", engine="openpyxl")
######################################################################



######################################################################
## RAW DATA SAP ######################################################
duckdb.register("SAP_ORDERS_LINEITEMS", sap_df)
print(f"SAP Loaded {len(sap_df)} rows")
######################################################################

## Query for unifying SAP Line Items. ################################
with open('./Querys/unify_SAP_LineItems.sql', 'r') as file:
        QUERY_SAP_ORDERS = file.read()

sap_orders_df = duckdb.query(QUERY_SAP_ORDERS).to_df()
duckdb.register("SAP_ORDERS", sap_orders_df)
print(f"SAP Orders {len(sap_orders_df)} (line items combined in 1 row)")

duckdb.execute("DROP VIEW IF EXISTS SAP_ORDERS_LINEITEMS")
######################################################################

## RAW DATA SFDC #####################################################
duckdb.register("SFDC_ORDERS", sfdc_df)
print(f"SFDC Loaded {len(sfdc_df)} rows")
######################################################################
######################################################################



## Outer with no inner Join query ####################################
with open('./Querys/joinOuterQuery.sql', 'r') as file:
        QUERY_OUTERJOINED_SAP_SFDC = file.read()

joinedOuterQuery = duckdb.query(QUERY_OUTERJOINED_SAP_SFDC).to_df()
print(f"Outer Data Query has {len(joinedOuterQuery)} unique rows")
save_to_excel(joinedOuterQuery,"OuterElements")
######################################################################
## Inner Join query on 'SAP Order Number' and 'Sales Document'########

# Read the SQL query from file
with open('./Querys/joinInnerQuery.sql', 'r') as file:
    QUERY_JOINED_SAP_SFDC = file.read()

# Execute the query and save to a DuckDB table
duckdb.execute(f"""
    CREATE OR REPLACE TABLE joined_sap_sfdc AS
    {QUERY_JOINED_SAP_SFDC}
""")

# Optional: Load into a DataFrame and export to Excel
joinedInnerQuery = duckdb.query("SELECT * FROM joined_sap_sfdc").to_df()

print(f"Joined Query has {len(joinedInnerQuery)} unique rows")
print(joinedInnerQuery.dtypes)

# Save to Excel
save_to_excel(joinedInnerQuery, "InnerElements")

######################################################################

## Amount Difference #################################################
with open('./Querys/amountDifference.sql', 'r') as file:
        QUERY_DIFFERENCEAMMOUNT_SAP_SFDC = file.read()

amountDifference = duckdb.query(QUERY_DIFFERENCEAMMOUNT_SAP_SFDC).to_df()
print(f"Amount Difference has {len(amountDifference)} unique rows")
print(amountDifference.dtypes)
save_to_excel(amountDifference,"AmountDifference")
######################################################################

## Payment Terms  ####################################################
with open('./Querys/paymentTerm.sql', 'r') as file:
        QUERY_PAYMENTTERM_SAP_SFDC = file.read()

paymentTermDifference = duckdb.query(QUERY_PAYMENTTERM_SAP_SFDC).to_df()
print(f"Payment Difference has {len(paymentTermDifference)} unique rows")
print(paymentTermDifference.dtypes)
save_to_excel(paymentTermDifference,"PayTerm Difference")
######################################################################

## TaxNumber Terms  ####################################################
with open('./Querys/taxNumberDifference.sql', 'r') as file:
        QUERY_TAXNUMBERDIFFERENCE_SAP_SFDC = file.read()

taxNumberDifference = duckdb.query(QUERY_PAYMENTTERM_SAP_SFDC).to_df()
print(f"TaxNumber Difference has {len(taxNumberDifference)} unique rows")
print(taxNumberDifference.dtypes)
save_to_excel(taxNumberDifference,"Tax Number Difference")
######################################################################

## Order Terms  ####################################################
with open('./Querys/orderTypeDifference.sql', 'r') as file:
        QUERY_ORDERTYPEDIFFERENCE_SAP_SFDC = file.read()

orderTypeDifference = duckdb.query(QUERY_ORDERTYPEDIFFERENCE_SAP_SFDC).to_df()
print(f"Order Type Difference has {len(orderTypeDifference)} unique rows")
print(orderTypeDifference.dtypes)
save_to_excel(orderTypeDifference,"Order Type  Difference")
######################################################################


## TaxNumber Terms  ####################################################
with open('./Querys/territoryDifference.sql', 'r') as file:
        QUERY_TERRITORYDIFFERENCE_SAP_SFDC = file.read()

territtoryDifference = duckdb.query(QUERY_TERRITORYDIFFERENCE_SAP_SFDC ).to_df()
print(f"Territory Difference has {len(territtoryDifference)} unique rows")
print(territtoryDifference.dtypes)
save_to_excel(territtoryDifference,"Territory Difference")
######################################################################

if (0):
    ## Show all tables
    tables = duckdb.execute("SHOW TABLES").fetchall()
    # Print schema for each table
    for (table_name,) in tables:
        print(f"Schema for table: {table_name}")
        schema = duckdb.execute(f"DESCRIBE {table_name}").fetchall()
        for column in schema:
             print(column)
        print("/n")


