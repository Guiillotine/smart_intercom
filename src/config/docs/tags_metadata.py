class TagsMetadata:
    @staticmethod
    def get_tags_metadata() -> list[dict[str, str]]:
        return [
            {
                "name": "User",
                "description": "Account info"
            },
            {
                "name": "Employees",
                "description": "Employee management"
            },
        ]
