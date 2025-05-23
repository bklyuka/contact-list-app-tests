get_contacts_schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "array",
    "items": [
        {
            "type": "object",
            "properties": {
                "_id": {
                    "type": "string"
                },
                "firstName": {
                    "type": "string"
                },
                "lastName": {
                    "type": "string"
                },
                "email": {
                    "type": "string"
                },
                "birthdate": {
                    "type": "string"
                },
                "phone": {
                    "type": "string"
                },
                "street1": {
                    "type": "string"
                },
                "street2": {
                    "type": "string"
                },
                "city": {
                    "type": "string"
                },
                "stateProvince": {
                    "type": "string"
                },
                "postalCode": {
                    "type": "string"
                },
                "country": {
                    "type": "string"
                },
                "owner": {
                    "type": "string"
                },
                "__v": {
                    "type": "integer"
                }
            },
            "required": [
                "_id",
                "firstName",
                "lastName",
                "owner",
                "__v"
            ]
        }
    ]
}

contact_schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "properties": {
        "_id": {
            "type": "string"
        },
        "firstName": {
            "type": "string"
        },
        "lastName": {
            "type": "string"
        },
        "email": {
            "type": "string"
        },
        "birthdate": {
            "type": "string"
        },
        "phone": {
            "type": "string"
        },
        "street1": {
            "type": "string"
        },
        "street2": {
            "type": "string"
        },
        "city": {
            "type": "string"
        },
        "stateProvince": {
            "type": "string"
        },
        "postalCode": {
            "type": "string"
        },
        "country": {
            "type": "string"
        },
        "owner": {
            "type": "string"
        },
        "__v": {
            "type": "integer"
        }
    },
    "required": [
        "_id",
        "firstName",
        "lastName",
        "owner",
        "__v"
    ]
}
