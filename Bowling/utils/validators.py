from werkzeug.exceptions import BadRequest

def validate_input(data):
    """Validate the input data."""
    if not isinstance(data, dict):
        raise BadRequest("Input must be a JSON object.")

    if "rolls" not in data:
        raise BadRequest("Missing 'rolls' key in input.")

    if not isinstance(data["rolls"], str):
        raise BadRequest("'rolls' must be a string.")

    if not data["rolls"]:
        raise BadRequest("'rolls' cannot be empty.")