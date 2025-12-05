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

querysPath = './sequences/LineItems.json'
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
    """Generate SQL from template with configuration"""
    try:
        template = Template(template_str)
        
        # Use .get() with defaults - much cleaner!
        substitutions = {
            "displaycolumns": get_display_columns(config.get("displaycolumns", "*")),
            "column1": config.get("column1", ""),
            "column2": config.get("column2", ""),
            "table1": config.get("table1", ""),
            "table2": config.get("table2",""),
            "registercolumn": config.get("registercolumn",""),
            "path": config.get("path", ""),
            "threshold": config.get("threshold", "0"),
            # Add all possible fields with defaults
        }
        
        # Remove empty values that might break the template
        substitutions = {k: v for k, v in substitutions.items() if v != ""}
        
        final = template.safe_substitute(**substitutions)
        return final
        
    except Exception as e:
        print(f"Error generating SQL template: {e}")
        return ""
    
def get_display_columns(display_cols):
    """Helper to format display columns"""
    if display_cols == "All" or display_cols == "*":
        return "*"
    elif isinstance(display_cols, list):
        return ",\n    ".join(f'"{col}"' for col in display_cols)
    else:
        return "*"

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
                query = generate_sql_from_template(readQueryTemplate('./querys/totalMatch.sql'), data)
                df = applyQuery(query)
        elif(data["typeofcomparison"]) == "Inner Join":  
                query = generate_sql_from_template(readQueryTemplate('./querys/joinInnerQuery.sql'),data)
                df = applyQuery(query) 
                if(data["registertable"]):
                        duckdb.register(view_name=data["registertable"], python_object=df)
        elif(data["typeofcomparison"]) == "Outer Join":  
                query = generate_sql_from_template(readQueryTemplate('./querys/joinOuterQuery.sql'),data)
                df = applyQuery(query) 
                if(data["registertable"]):
                        duckdb.register(view_name=data["registertable"], python_object=df)
        elif(data["typeofcomparison"] == "Amount Difference"):
                query = generate_sql_from_template(readQueryTemplate('./querys/amountDifference.sql'), data)
                df = applyQuery(query)
        elif(data["typeofcomparison"]) == "Read Excel Data":
                df = readExcel(data["path"])
                if(data["registertable"]):
                        duckdb.register(view_name=data["registertable"], python_object=df)
        elif(data["typeofcomparison"]) == "Custom":
                df = applyQuery(readQueryTemplate(data["path"]))
                if(data["registertable"]):
                        duckdb.register(view_name=data["registertable"], python_object=df)
        elif(data["typeofcomparison"]) == "Combine Two Columns":
                query = generate_sql_from_template(readQueryTemplate('./querys/combineTwoColumns.sql'),data)
                df = applyQuery(query)
                if(data["registertable"]):
                        duckdb.register(view_name=data["registertable"], python_object=df)
        elif(data["typeofcomparison"] == "Parcial Match"):
               query = generate_sql_from_template(readQueryTemplate('./querys/parcialMatch.sql'),data)
               df = applyQuery(query)
        elif(data["typeofcomparison"] == "Outer Join"):
               query = generate_sql_from_template(readQueryTemplate('./querys/joinOuterQuery.sql'),data)
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


for elm in document:
      appFlowControl(elm)



