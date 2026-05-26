class TagsMetadata:
    @staticmethod
    def get_tags_metadata() -> list[dict[str, str]]:
        return [
            {
                "name": "Auth",
                "description": "Auth methods"
            },
            {
                "name": "Users",
                "description": "Account info"
            },
            {
                "name": "Employees",
                "description": "Employee management"
            },
            {
                "name": "Visits",
                "description": "Visit management"
            },
            {
                "name": "Messages",
                "description": "Messages history management"
            },
            {
                "name": "Intercoms",
                "description": "Methods for intercom"
            }
        ]
