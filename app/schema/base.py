from pydantic import BaseModel, model_validator

from typing import Dict, Any


class F1BaseModel(BaseModel):
    @model_validator(mode="before")
    def handle_case_insensitive_fields(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        model_fields = cls.__fields__.keys()
        lower_to_field_mapping = {field.lower(): field for field in model_fields}
        new_values = {}
        if isinstance(values, dict):
            for key, value in values.items():
                key_lower = key.lower()
                if key_lower in lower_to_field_mapping:
                    new_key = lower_to_field_mapping[key_lower]
                    new_values[new_key] = value
                else:
                    new_values[key] = value
        else:
            for key in dir(values):
                if not key.startswith("_"):
                    value = getattr(values, key)
                    key_lower = key.lower()
                    if key_lower in lower_to_field_mapping:
                        new_key = lower_to_field_mapping[key_lower]
                        new_values[new_key] = value
                    else:
                        new_values[key] = value
        return new_values

