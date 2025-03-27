from dataclasses import dataclass
from typing import Optional

def infer_type(values):
    """Infer the best type for a field based on a list of values."""
    types = {type(v) for v in values if v is not None}

    if len(types) == 1:
        return next(iter(types)).__name__  # Use the single detected type
    elif len(types) > 1:
        return "str | int | float | bool"  # Mixed types, defaulting to union
    else:
        return "str"  # Default if empty

def generate_dataclass(name, data_list):
    """Generate a dataclass from a list of dictionaries."""
    all_keys = {key for d in data_list for key in d}
    field_types = {key: infer_type([d.get(key) for d in data_list]) for key in all_keys}

    # Determine which fields are optional
    optional_fields = {key for key in all_keys if any(d.get(key) is None for d in data_list)}

    # Separate required and optional fields
    required_fields = {key: field_types[key] for key in all_keys if key not in optional_fields}
    optional_fields = {key: field_types[key] for key in optional_fields}

    dataclass_code = f"@dataclass\nclass {name}:\n"

    # Add required fields first (no default values)
    for key, field_type in required_fields.items():
        dataclass_code += f"    {key}: {field_type}\n"

    # Add optional fields (defaulting to None)
    for key, field_type in optional_fields.items():
        dataclass_code += f"    {key}: Optional[{field_type}] = None\n"

    return dataclass_code

if __name__ == '__main__':
    # Example data
    data = [
        {"name": "Alice", "age": 25, "isEnabled": True},
        {"name": "Bob", "age": 30, "city": "New York"},
    ]

    # Generate dataclass code
    dataclass_code = generate_dataclass("Person", data)
    print(dataclass_code)
