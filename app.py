from flask import Flask, jsonify, request, abort
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)

# In-memory store; reset every restart
ITEMS: dict[str, dict[str, str]] = {}

OPENAPI_SPEC = {
    "openapi": "3.0.3",
    "info": {
        "title": "Simple Items API",
        "version": "1.0.0",
        "description": "CRUD-ish demo over an in-memory item store."
    },
    "paths": {
        "/items": {
            "get": {
                "summary": "List items",
                "responses": {
                    "200": {
                        "description": "Array of items",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "array",
                                    "items": {"$ref": "#/components/schemas/Item"}
                                }
                            }
                        }
                    }
                }
            },
            "post": {
                "summary": "Create item",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/NewItem"}
                        }
                    }
                },
                "responses": {
                    "201": {
                        "description": "Created item",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Item"}
                            }
                        }
                    },
                    "400": {"description": "Missing required fields"},
                    "409": {"description": "Item already exists"}
                }
            }
        },
        "/items/{item_id}": {
            "parameters": [
                {
                    "name": "item_id",
                    "in": "path",
                    "required": True,
                    "schema": {"type": "string"}
                }
            ],
            "get": {
                "summary": "Get single item",
                "responses": {
                    "200": {
                        "description": "Item found",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Item"}
                            }
                        }
                    },
                    "404": {"description": "Item not found"}
                }
            },
            "delete": {
                "summary": "Delete item",
                "responses": {
                    "200": {
                        "description": "Deleted item",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Item"}
                            }
                        }
                    },
                    "404": {"description": "Item not found"}
                }
            }
        }
    },
    "components": {
        "schemas": {
            "Item": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "name": {"type": "string"}
                },
                "required": ["id", "name"]
            },
            "NewItem": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "name": {"type": "string"}
                },
                "required": ["id", "name"]
            }
        }
    }
}

SWAGGER_URL = "/docs"
API_URL = "/openapi.json"
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={"app_name": "Simple Items API"}
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


@app.get("/openapi.json")
def openapi_spec():
    return jsonify(OPENAPI_SPEC)


@app.get("/items")
def list_items():
    return jsonify(list(ITEMS.values()))


@app.get("/items/<item_id>")
def get_item(item_id: str):
    item = ITEMS.get(item_id)
    if not item:
        abort(404, description="Item not found")
    return jsonify(item)


@app.post("/items")
def create_item():
    data = request.get_json(silent=True) or {}
    item_id = data.get("id")
    name = data.get("name")
    if not item_id or not name:
        abort(400, description="Fields 'id' and 'name' are required")
    if item_id in ITEMS:
        abort(409, description="Item already exists")
    ITEMS[item_id] = {"id": item_id, "name": name}
    return jsonify(ITEMS[item_id]), 201


@app.delete("/items/<item_id>")
def delete_item(item_id: str):
    if item_id not in ITEMS:
        abort(404, description="Item not found")
    deleted = ITEMS.pop(item_id)
    return jsonify(deleted)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
