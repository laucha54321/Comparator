import pandas as pd
import duckdb
import os 
import json
from string import Template

from schemaValidator import validateJson
from colorama import init, Fore, Back, Style

# Initialize colorama (auto-reset, works on Windows)
init(autoreset=True)

# Define some convenient color constants (optional)
GREEN = Fore.GREEN
YELLOW = Fore.YELLOW
RED = Fore.RED
CYAN = Fore.CYAN
MAGENTA = Fore.MAGENTA
BOLD = Style.BRIGHT
RESET = Style.RESET_ALL

import sys
import traceback

def wait_on_exit():
    """Pause for user input if the script is compiled to an executable."""
    if getattr(sys, 'frozen', False):
        input("\nPress Enter to exit...")

def global_exception_handler(exc_type, exc_value, exc_traceback):
    """Catch any unhandled exception, print it nicely, and wait for Enter."""
    print("\n" + "="*50)
    print("⚠️  AN UNEXPECTED ERROR OCCURRED:")
    print(f"Error Type: {exc_type.__name__}")
    print(f"Message: {exc_value}")
    print("\n--- Full Traceback ---")
    traceback.print_tb(exc_traceback)
    print("="*50)
    wait_on_exit()

# Override Python's default exception handler
sys.excepthook = global_exception_handler


print(f"""
{BOLD}{CYAN}
   _____                                      _             
  / ____|                                    | |            
 | |     ___  _ __ ___  _ __   __ _ _ __ __ _| |_ ___  _ __ 
 | |    / _ \| '_ ` _ \| '_ \ / _` | '__/ _` | __/ _ \| '__|
 | |___| (_) | | | | | | |_) | (_| | | | (_| | || (_) | |   
  \_____\___/|_| |_| |_| .__/ \__,_|_|  \__,_|\__\___/|_|   
                       | |                                  
                       |_|                                  
{RESET}
{YELLOW}                  -- by Laureano Oliva --{RESET}

  Read-Me: https://github.com/laucha54321/Comparator
""")

DEBUGING = False

### ---- NEW MENU: SELECT SEQUENCE FILE ----
sequences_folder = './sequences'

# 1. Check if the folder exists
if not os.path.exists(sequences_folder):
    print(f"ERROR: Folder '{sequences_folder}' not found!")
    print("Please make sure the 'sequences' folder is in the same directory as this program.")
    sys.exit(1)

# 2. List all .json files in the folder
json_files = []
for file in os.listdir(sequences_folder):
    if file.endswith('.json'):
        json_files.append(file)

# 3. If no JSON files found, exit
if not json_files:
    print(f"ERROR: No JSON sequence files found in '{sequences_folder}'!")
    sys.exit(1)

# 4. Display the menu
print("\n" + "="*50)
print("     AVAILABLE SEQUENCE FILES")
print("="*50)
for idx, filename in enumerate(json_files, start=1):
    print(f"  [{idx}] {filename}")
print("  [0] Exit / Cancel")
print("="*50)

# 5. Get user selection
while True:
    try:
        choice = input(f"\nSelect a sequence (1-{len(json_files)}) or 0 to exit: ")
        choice_num = int(choice)
        
        if choice_num == 0:
            print("Exiting program.")
            sys.exit(0)
        elif 1 <= choice_num <= len(json_files):
            selected_file = json_files[choice_num - 1]
            break
        else:
            print(f"Invalid choice. Please enter a number between 0 and {len(json_files)}.")
    except ValueError:
        print("Invalid input. Please enter a number.")

# 6. Set the path to the selected file
querysPath = os.path.join(sequences_folder, selected_file)
print(f"\n>>> Selected: {selected_file}\n")

### ---- END OF MENU ----

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
                

        print(f"\n============================================================\n| {BOLD}{CYAN}{data["name"].upper()}{RESET} |{BOLD}{CYAN} {data["typeofcomparison"]}. {RESET}|\n============================================================\n")
        


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
                if(data["registertable"]):
                        duckdb.register(view_name=data["registertable"], python_object=df)
        elif data["typeofcomparison"] == "Read Excel Data":
            df = readExcel(data["path"])
            reg_name = data.get("registertable")
            if reg_name:
                # Verificar si la tabla ya existe (como tabla persistente)
                existing_tables = duckdb.execute("SHOW TABLES").fetchdf()["name"].tolist()
                if reg_name in existing_tables:
                    # Append: la tabla ya existe, insertamos los nuevos registros
                    duckdb.execute(f"INSERT INTO {reg_name} SELECT * FROM df")
                    print(f"Appended {len(df)} rows to table '{reg_name}'")
                else:
                    # Crear la tabla por primera vez
                    duckdb.execute(f"CREATE TABLE {reg_name} AS SELECT * FROM df")
                    print(f"Tabel '{reg_name}' created with {len(df)} rows")

        elif(data["typeofcomparison"]) == "Delete Row":
                query = generate_sql_from_template(readQueryTemplate('./querys/deleteRow.sql'), data)
                df = applyQuery(query)
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
        
        try:
                print(f"{data["name"].upper()} has {len(df)} unique rows")
        except:
               print("error at print statement.")

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

wait_on_exit() 
