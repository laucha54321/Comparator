
import pandas as pd
import duckdb
import os 
import json
from string import Template

from schemaValidator import validateJson


print(r"""
   _____                                      _             
  / ____|                                    | |            
 | |     ___  _ __ ___  _ __   __ _ _ __ __ _| |_ ___  _ __ 
 | |    / _ \| '_ ` _ \| '_ \ / _` | '__/ _` | __/ _ \| '__|
 | |___| (_) | | | | | | |_) | (_| | | | (_| | || (_) | |   
  \_____\___/|_| |_| |_| .__/ \__,_|_|  \__,_|\__\___/|_|   
                       | |                                  
                       |_|                                  
      
                
                  -- by Laureano Oliva --                                             
""")

DEBUGING = False

querysPath = './sequences/Orders.json'
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
        column1=config["column1"],
        column2=config["column2"]
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

def appFlowControl(data):
        def applyQuery(query):
                try: 
                        result = duckdb.query(query).to_df()
                        if(DEBUGING): print(f"\n --- QUERY ------------------------------ \n {query} \n ----------------------------------------")
                        return result
                except Exception as e:
                        print(f"There was an error while executing {data["name"].upper()}")
                        print(f"Error message: \n{e}")
                return
                

        print(f"\n============================================================\n| {data["name"].upper()} | {data["typeofcomparison"]}. |\n============================================================\n")
        
        if(data["typeofcomparison"]) == "Total Match":
                query = generate_sql_from_template(readQueryTemplate('./Querys/totalMatch.sql'), data)
                df = applyQuery(query)  
        elif(data["typeofcomparison"]) == "Inner Join":  
                query = generate_sql_from_template(readQueryTemplate('./Querys/joinInnerQuery.sql'),data)
                df = applyQuery(query) 
                if(data["registertable"]):
                        duckdb.register(view_name=data["registertable"], python_object=df)
        elif(data["typeofcomparison"]) == "Read Excel Data":
                df = readExcel(data["path"])
                if(data["registertable"]):
                        duckdb.register(view_name=data["registertable"], python_object=df)
        elif(data["typeofcomparison"]) == "Custom":
                df = applyQuery(readQueryTemplate(data["path"]))
                if(data["registertable"]):
                        duckdb.register(view_name=data["registertable"], python_object=df)
        elif(data["typeofcomparison"]) == "Combine Two Columns":
                query = generate_sql_from_template(readQueryTemplate('./Querys/combineTwoColumns.sql'),data)
                df = applyQuery(query)
                if(data["registertable"]):
                        duckdb.register(view_name=data["registertable"], python_object=df)
        elif(data["typeofcomparison"] == "Parcial Match"):
               query = generate_sql_from_template(readQueryTemplate('./Querys/parcialMatch.sql'),data)
               df = applyQuery(query)
        elif(data["typeofcomparison"] == "Outer Join"):
               query = generate_sql_from_template(readQueryTemplate('./Querys/joinOuterQuery.sql'),data)
               df = applyQuery(query)
                 
        else:
                print(f"Error Message: No query applied. The query type {data["typeofcomparison"]} does not exists. ")
                return
        
        print(f"{data["name"].upper()} has {len(df)} unique rows")

        if data["savetoexcel"]:
                try:
                        save_to_excel(df,f"{data["name"]}")
                        print(f"Data registered to excel file on sheet \"{data["name"]}\".")
                        
                except Exception as e:
                        print(f"Error Message:\n {e}")
        
        print("============================================================\n")
                
def readExcel(path):
        try:
               print(f"Reading file {path}")
               result =  pd.read_excel(path)
               return result
        except Exception as e: 
               print(f"Error Message: \n {e}")

""" ## Read Files#########################################################
sap_df = readExcel("./Database/Orders/SAP - ZSD18A_ARG/Orders.xlsx")
sfdc_df = readExcel("./Database/Orders/SFDC - Access - Integrity Order Report/Access - Integrity Order Report-2025-06-26-09-20-03.xlsx")
######################################################################


######################################################################
## RAW DATA SAP ######################################################
duckdb.register("SAP_ORDERS_LINEITEMS", sap_df)
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
######################################################################
##################################################################### """

for elm in document:
      appFlowControl(elm)



