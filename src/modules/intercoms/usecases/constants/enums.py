from src.common.constants import CommonEnums
from src.modules.dialogues.constants import DialogueEnums
from src.modules.messages.constants import MessageEnums
from src.modules.visits.constants import VisitEnums


class IntercomUCEnums:
    def __init__(
        self,
        common_enums: CommonEnums,
        visit_common_enums: VisitEnums,
        message_common_enums: MessageEnums,
        dialogue_common_enums: DialogueEnums,
    ):
        self.Common = common_enums
        self.Visit = visit_common_enums
        self.Message = message_common_enums
        self.Dialogue = dialogue_common_enums
