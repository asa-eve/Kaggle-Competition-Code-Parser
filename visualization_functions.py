import re
import pkgutil

#######################################################################

def get_valid_module_names():
    # Get a set of valid Python module names
    valid_module_names = set()
    for _, module_name, _ in pkgutil.iter_modules():
        valid_module_names.add(module_name)
    return valid_module_names

#######################################################################

def clean_library_names(library_names):
    cleaned_names = []

    # Get valid Python module names
    valid_module_names = get_valid_module_names()

    # Compile a regex pattern to match standalone words
    pattern = re.compile(r'^[a-zA-Z_][a-zA-Z0-9_]*$')

    for name in library_names:
        # Check if the name is a valid Python module name
        if name in valid_module_names:
            cleaned_names.append(name)
        else:
            # Split the string by ".", ":", or ";"
            parts = re.split(r'[.:;]', name)
            cleaned_names.append(parts[0])
            
#             cleaned_parts = []

#             for part in parts:
#                 # Check if the part is a standalone word
#                 match = pattern.match(part)
#                 if match:
#                     cleaned_parts.append(part)

#             # If there's only one part and it's a valid module name, append it
#             if len(cleaned_parts) == 1 and cleaned_parts[0] in valid_module_names:
#                 cleaned_names.append(cleaned_parts[0])

    return cleaned_names


#######################################################################

def clean_sublibrary_names(library_names):
    cleaned_names = []

    # Get valid Python module names
    valid_module_names = get_valid_module_names()

    # Compile a regex pattern to match standalone words
    pattern = re.compile(r'^[a-zA-Z_][a-zA-Z0-9_]*$')

    for name in library_names:
        # Split the string by ".", ":", or ";"
        parts = re.split(r'[.:;]', name)
        cleaned_parts = []

        for part in parts:
            # Check if the part is a valid Python module name
            if part in valid_module_names:
                cleaned_parts.append(part)
            else:
                # Check if the part is a standalone word
                match = pattern.match(part)
                if match:
                    cleaned_parts.append(part)

        # Join the cleaned parts back into a string and append it to the cleaned_names list
        cleaned_name = ".".join(cleaned_parts)
        if cleaned_name:
            cleaned_names.append(cleaned_name)

    return cleaned_names


#######################################################################

def count_strings(strings, unique_strings, NO_SUBLIBRARIES):
    if NO_SUBLIBRARIES:
        for idx in range(len(strings)):
            parts = re.split(r'[.:;]', strings[idx])
            strings[idx] = parts[0]
    
    string_dict = {}

    for unique_string in unique_strings:
        string_dict[unique_string] = strings.count(unique_string)

    return string_dict