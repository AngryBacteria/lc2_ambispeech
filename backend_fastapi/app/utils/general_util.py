def print_attributes(obj, indent=0):
    """Recursively print attributes and their values of a Python object."""

    # Base cases to stop the recursion
    if isinstance(obj, (int, float, str, bytes, bool, type(None))):
        return

    # List of built-in attributes that we don't want to print
    builtin_attrs = set(dir(type("dummy string")))

    for attr in dir(obj):
        if attr.startswith("__") and attr.endswith("__"):
            continue  # Skip dunder attributes
        if attr in builtin_attrs:
            continue  # Skip built-in attributes
        try:
            value = getattr(obj, attr)
            print("  " * indent + f"{attr}: {value}")
        except Exception as e:
            print("  " * indent + f"{attr}: <Error: {e}>")
