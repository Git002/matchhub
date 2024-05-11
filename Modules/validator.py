import jsonschema

INVALID_SCHEMA_MESSAGE = {
    "message": "Bad request: wrong/missing fields in request body",
    "data": [],
}


def validate_schema(instance, schema):
    try:
        jsonschema.validate(instance=instance, schema=schema)
        return True
    except jsonschema.exceptions.ValidationError as err:
        print(err)
        return False
