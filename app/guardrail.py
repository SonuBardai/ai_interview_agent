import json
from typing import Tuple, Any


def validate_json_output(result: str) -> Tuple[bool, Any]:
    """Validate that the output is valid JSON."""
    if isinstance(result, dict):
        return (True, result)
    if isinstance(result, list):
        return (True, result)
    try:
        json_data = json.loads(result)
        return (True, json_data)
    except json.JSONDecodeError as e:
        print("Failed json decode error input: ", result)
        print("ERROR: ", e)
        return (False, {"error": str(e), "code": "JSON_DECODE_ERROR"})
    except Exception as e:
        print("Failed validate_json_output input: ", result)
        print("ERROR: ", e)
        return (False, {"error": str(e), "code": "UNKNOWN_ERROR"})


def validate_json_dict_output(result) -> Tuple[bool, Any]:
    return validate_json_output(result.json_dict)


def validate_raw_output(result) -> Tuple[bool, Any]:
    return validate_json_output(result.raw)


def chain_validations(*validators):
    def combined_validator(result):
        for validator in validators:
            success, data = validator(result)
            if not success:
                return (False, data)
            result = data
        return (True, result)

    return combined_validator
