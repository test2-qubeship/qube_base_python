"""
swagger parameters definitions
"""
header_ex = {
    "type": "string",
    "description": "Custom header that is expected as part of the request",
    "name": "Authorization",
    "in": "header",
    "required": True
}

path_ex = {
    "type": "string",
    "description": "This is the part of the URL",
    "name": "id",
    "in": "path",
    "required": True
}

query_ex = {
    "type": "string",
    "description": "Query string appended to the URL",
    "name": "sth",
    "in": "query",
    "required": False
}
