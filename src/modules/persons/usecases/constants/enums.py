from src.modules.persons.constants import PersonEnums
from src.modules.persons.schemas.constants import PersonSchemaEnums


class EmployeeUCEnums:
    """
    Aggregates enums used in the EmployeeUC (Employee Use Case) layer.
    """

    def __init__(
        self,
        person_common_enums: PersonEnums,
        person_schema_enums: PersonSchemaEnums,
    ):
        self.Person = person_common_enums
        self.PersonSchema = person_schema_enums
        