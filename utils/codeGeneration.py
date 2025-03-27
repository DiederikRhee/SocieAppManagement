from dataclasses import dataclass
from typing import Optional
from datetime import datetime
import re

# Regex for detecting ISO 8601 timestamps
ISO_TIMESTAMP_REGEX = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})?$"
)

def infer_type(values):
    """Infer the most specific type for a field based on given values."""
    types = set()
    
    for v in values:
        if v is None:
            continue
        if isinstance(v, bool):
            types.add("bool")
        elif isinstance(v, int):
            types.add("int")
        elif isinstance(v, float):
            types.add("float")
        elif isinstance(v, str):
            # Check for boolean-like strings
            if v.lower() in {"true", "false"}:
                types.add("bool")
            # Check for ISO timestamps
            elif ISO_TIMESTAMP_REGEX.match(v):
                types.add("datetime")
            # Otherwise, it's a normal string
            else:
                types.add("str")

    if len(types) == 1:
        return next(iter(types))  # Use the detected type
    elif "float" in types and "int" in types:
        return "float"  # If both int and float exist, use float
    elif types:
        return "str | int | float | bool | datetime"  # Mixed types fallback
    else:
        return "str"  # Default if empty

def generate_dataclass(name, data_list):
    """Generate a dataclass from a list of dictionaries."""
    all_keys = {key for d in data_list for key in d}
    field_types = {key: infer_type([d.get(key) for d in data_list]) for key in all_keys}

    # Separate required and optional fields
    optional_fields = {key for key in all_keys if any(d.get(key) is None for d in data_list)}
    required_fields = {key for key in all_keys if key not in optional_fields}

    dataclass_code = f"@dataclass\nclass {name}:\n"

    # Add required fields first (no default values)
    for key in required_fields:
        dataclass_code += f"    {key}: {field_types[key]}\n"

    # Add optional fields (defaulting to None)
    for key in optional_fields:
        dataclass_code += f"    {key}: Optional[{field_types[key]}] = None\n"

    return dataclass_code

if __name__ == '__main__':
    # Example data
    data = [
        {"name": "Alice", "age": 25, "created_at": "2024-03-27T12:00:00Z", "isEnabled": True},
        {"name": "Bob", "age": 30, "city": "New York", "created_at": "2024-03-26T14:30:00Z"},
        {"name": "Charlie", "age": 40, "created_at": None},  # Missing timestamp
    ]

    # Generate dataclass code
    dataclass_code = generate_dataclass("Person", data)
    print(dataclass_code)
