import re
import json

def read_prisma_file():
    with open("app.prisma", "r") as file:
        return file.read()

def save_json(properties):
    with open("prisma.json", "w") as json_file:
        json.dump(properties, json_file, indent=4)

model_name_regex = re.compile(r"model\s+(\w+)\s+\{", re.MULTILINE)
model_names = model_name_regex.findall(read_prisma_file())

model_regex = re.compile(r"model\s+(\w+)\s+\{([^}]*)\}", re.MULTILINE)
property_regex = re.compile(r"^\s*(\w+)\s+(\w+)(\?)?(\[])?", re.MULTILINE)

models = model_regex.findall(read_prisma_file())
properties = []
model_properties = []

for model in models:
    model_name, model_body = model
    property_matches = property_regex.findall(model_body)
    for match in property_matches:
        name, type, is_optional, is_array = match
        model_properties.append({
            "name": name,
            "type": type,
            "isOptional": bool(is_optional),
            "isArray": bool(is_array)
        })
    properties.append({
        "modelName": model_name,
        "properties": model_properties
    })

save_json(properties)