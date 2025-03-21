import json
from jsonschema import Draft202012Validator, validators
from referencing import Registry, Resource
import importlib.resources
import geysergen
import os
from os import listdir
from os.path import isfile, join
root_dir = importlib.resources.files(geysergen)
base_file = root_dir.joinpath("./schemas/generic.schema.json")
refs = [root_dir.joinpath("./schemas/helpers.schema.json"),root_dir.joinpath("./schemas/special.schema.json")]
interface_dir = str(root_dir.joinpath("./schemas/interfaces/"))

def extend_with_default_(validator_class):
    validate_properties = validator_class.VALIDATORS["properties"]

    def set_defaults(validator, properties, instance, schema):
        for property, subschema in properties.items():
            if "default" in subschema:
                instance.setdefault(property, subschema["default"])
        for error in validate_properties(
            validator, properties, instance, schema,
        ):
            yield error

    return validators.extend(
        validator_class, {"properties" : set_defaults},
    )


DefaultValidatingValidator = extend_with_default_(Draft202012Validator)

def get_registry() -> Registry:
    #we need to create the registry of schema files 
    registry = Registry()
    for file in refs:
        registry = Resource.from_contents(json.load(open(file))) @ registry 

    for file in [join(interface_dir, f) for f in listdir(interface_dir) if isfile(join(interface_dir, f))]:
        registry = Resource.from_contents(json.load(open(file))) @ registry
    return registry

def validate_json(json_data) -> None:
    base_schema = json.load(open(base_file))
    Draft202012Validator(base_schema,registry=get_registry()).validate(json_data)

def populate_defaults(interface_list:list) -> list:
    for inter in interface_list:
        if os.path.isfile(interface_dir+"/"+inter['type']+".schema.json"):
            with open(interface_dir+"/"+inter['type']+".schema.json") as temp:
                type_schema = json.load(temp)
                DefaultValidatingValidator(type_schema,registry=get_registry()).validate(inter)
    return interface_list
