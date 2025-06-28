import pandas as pd
import duckdb
import os 
import json
from string import Template

from schemaValidator import validateJson

DEBUGING = False

querysPath = './querys.json'
querysSchema = './querys-schema.json'

validateJson(document_path=querysPath,schema=querysSchema)

### Save to excel function ####
def save_to_excel(df, sheet_name):
    file_path = "result.xlsx"
    if not os.path.exists(file_path):
        with pd.ExcelWriter(file_path, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name=sheet_name)
    else:
        with pd.ExcelWriter(file_path, mode='a', engine="openpyxl", if_sheet_exists='replace') as writer:
            df.to_excel(writer, index=False, sheet_name=sheet_name)

with open(querysPath) as f:
        document = json.load(f)

def generate_sql_from_template(template_str, config):
    if(config["displaycolumns"] == "All"):
        display_columns = "*"
    else:
        display_columns = ",\n    ".join(f'"{col}"' for col in config["displaycolumns"])
    template = Template(template_str)
    final = template.substitute(
        displaycolumns=display_columns,
        sapcolumn=config["sapcolumn"],
        sfdccolumn=config["sfdccolumn"]
    )
    return final

def readQueryTemplate(pathtoquery):
        try:
                with open(pathtoquery, 'r') as file:
                        totalMatchQuery = file.read()
                return totalMatchQuery
        except Exception:
              print(f"There was an Issue with the {pathtoquery} query.")
              return

def queryFlowControl(data):
        def applyQuery(query):
                try: 
                        result = duckdb.query(query).to_df()
                        if(DEBUGING): print(f"\n --- QUERY ------------------------------ \n {query} \n ----------------------------------------")
                        return result
                except Exception as e:
                        print(f"There was an error while executing {data["name"].upper()}")
                        print(f"Error message: {e}")
                return
                

        print(f"\n========================================\nStarting comparisson {data["name"].upper()}.")
        if(data["typeofcomparison"]) == "Total Match":
                query = generate_sql_from_template(readQueryTemplate('./Querys/totalMatch.sql'), data)
                result = applyQuery(query)
        elif(data["typeofcomparison"]) == "Inner Join":  
                query = generate_sql_from_template(readQueryTemplate('./Querys/joinInnerQuery.sql'),data)
                result = applyQuery(query)
        else:
                print("Query not applied")

        if "registertable" in data:
                duckdb.register(data["registertable"], result)

        save_to_excel(result,f"{data["name"]}")
        print(f"{data["name"].upper()} has {len(result)} unique rows")
        print(f"========================================")

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

for elm in document:
      queryFlowControl(elm)