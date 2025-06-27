import json
from jsonschema import validate
from jsonschema.exceptions import ValidationError

def validateJson(document_path, schema):
    'Document and schema can be a path to a json file'
    with open(document_path) as f:
        document = json.load(f)

    with open(schema) as f:
        schema = json.load(f)
    
    try:
        validate(instance=document,schema=schema)
        print(f"JSON File ({document_path}) schema validation SUCCESSFUL")
    except ValidationError as e:
        print("Json File Schema Error. Review the Schema of the file.")
        print(f"Error Message: {e.message}")
