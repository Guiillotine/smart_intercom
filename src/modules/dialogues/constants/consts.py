from typing import ClassVar

from src.common.constants.consts import LanguageConsts
from src.common.constants.enums import LanguageEnum
from src.modules.dialogues.constants.enums import DialogueModeEnum, BotMessageEnum
from src.modules.dialogues.schemas.dialogue import WantToEnterBotAnswer, \
    DetectLanguageBotAnswer, VisitorCallEmployeeBotAnswer, DialogueConfig, \
    GoalDialogueBotAnswer, GrantAccessDialogueBotAnswer


class BotMessageConst:
  MESSAGE_LANG_MAP: ClassVar[dict[tuple[BotMessageEnum, LanguageEnum], str]] = {
      # RU
      (BotMessageEnum.HELLO, LanguageEnum.RU): "Здравствуйте. Вы позвонили в домофон компании Эстэсис. Пожалуйста, назовите цель вашего визита.",
      (BotMessageEnum.RECOGNIZED, LanguageEnum.RU): "Узнала вас. Сейчас я вызову сотрудника.",
      (BotMessageEnum.ERROR, LanguageEnum.RU): "Извините, произошла ошибка. Сейчас я вызову сотрудника.",
      (BotMessageEnum.ACCESS_GRANTED, LanguageEnum.RU): "Добро пожаловать в компанию Эстэсис.",
      (BotMessageEnum.ACCESS_NOT_GRANTED, LanguageEnum.RU): "Извините, но мы не можем открыть дверь. Всего доброго.",
      (BotMessageEnum.WANT_TO_ENTER_QUESTION, LanguageEnum.RU): "Настаиваете ли вы на входе в компанию Эстэсис?",
      (BotMessageEnum.CALL_EMPLOYEE, LanguageEnum.RU): "Сейчас я уведомлю сотрудника о вашем визите. Это займёт некоторое время.",
      (BotMessageEnum.GOODBYE, LanguageEnum.RU): "До свидания, всего доброго.",
      # EN
      (BotMessageEnum.HELLO, LanguageEnum.EN): "Hello. You have reached the Estesis intercom. Please state the purpose of your visit.",
      (BotMessageEnum.RECOGNIZED, LanguageEnum.EN): "I recognized you. I'll call a staff member now.",
      (BotMessageEnum.ERROR, LanguageEnum.EN): "Sorry, there was an error. I'll call a member of staff right now.",
      (BotMessageEnum.ACCESS_GRANTED, LanguageEnum.EN): "Welcome to Estesis.",
      (BotMessageEnum.ACCESS_NOT_GRANTED, LanguageEnum.EN): "Sorry, but we can't open the door. Goodbye.",
      (BotMessageEnum.WANT_TO_ENTER_QUESTION, LanguageEnum.EN): "Do you still want to enter the Estesis office?",
      (BotMessageEnum.CALL_EMPLOYEE, LanguageEnum.EN): "I'll notify a member of staff about your visit now. This will take some time.",
      (BotMessageEnum.GOODBYE, LanguageEnum.EN): "Goodbye, have a nice day.",
  }

  @classmethod
  def get(cls, message_type: BotMessageEnum, lang: LanguageEnum) -> str:
      return cls.MESSAGE_LANG_MAP.get(
          (message_type, lang),
          cls.MESSAGE_LANG_MAP[(message_type, LanguageConsts.DEFAULT_LANG)],
      )


class PromptConst:
  DIALOGUE_LANGUAGE_PROMPT: ClassVar[str] = """
Текущий язык диалога: {}.
Если среди полей ответа есть "content", то текст в этом поле должен быть на этом языке.
"""

  DETECT_LANGUAGE_INITIAL_PROMPT: ClassVar[str] = f"""
Определи язык сообщения пользователя.

Допустимые значения: {LanguageEnum.get_langs_str_list()}.

Если язык невозможно надёжно определить, верни текущий язык диалога.

Верни только JSON без markdown и без дополнительных пояснений.

Поля ответа:
- lang: язык сообщения пользователя.
"""

  DETECT_LANGUAGE_SCHEMA_PROMPT: ClassVar[str] = """
Верни строго JSON-объект следующего вида:
{
  "lang": "ru"
}
Не добавляй никаких пояснений до или после JSON.
"""

  CALL_EMPLOYEE_INITIAL_PROMPT: ClassVar[str] = f"""
Ты — голосовой помощник умного домофона компании Эстэсис, расположенной в бизнес-центре.

Тебе пришло сообщение от посетителя. Если посетитель в сообщении явно просит позвать сотрудника, хочет говорить с человеком, а не с голосовым помощником, установи call_employee в true.
Во всех остальных случаях устанавливай call_employee в false.
Не устанавливай call_employee в true только потому, что посетитель раздражён, говорит эмоционально или недоволен.

Поля ответа:
- call_employee: true, только если посетитель явно попросил вызвать человека, хочет разговаривать с настоящим человеком; иначе всегда устанавливай false.
"""

  CALL_EMPLOYEE_SCHEMA_PROMPT: ClassVar[str] = """
Верни строго JSON-объект следующего вида:
{
  "call_employee": false
}
Не добавляй никаких пояснений до или после JSON.
"""

  GOAL_INITIAL_PROMPT: ClassVar[str] = f"""
Ты - голосовой помощник IT компании Эстэсис, расположенной в бизнес-центре.

Твоя задача - кратко, вежливо и понятно общаться с посетителем и выяснить цель его визита.

Контекст:
- В офис компании обычно приходят сотрудники. Сотрудники компании - люди, связанные с IT сферой (например: программисты, менеджеры, аналитики).
- Также могут приходить ожидаемые посетители: курьеры, доставка воды, еды, документов, техники, подрядчики, кандидаты на собеседование и другие приглашённые люди.
- Иногда посетители ошибаются входом и хотят попасть не в компанию Эстэсис, а в бизнес-центр.
- Если цель визита связана с получением услуг, не относящихся к IT-компании, то такая цель не относится к компании Эстэсис.
- Если цель не относится к компании Эстэсис - возможно посетитель ошибся входом.
- В ответе посетитителю не проговаривай цель его визита.
- Не обещай ничего лишнего: если цель понятна - просто скажи, что ты поняла посетителя. Например: не обещай, что сообщишь сотруднику. Тебе нужно только понять цель.

Правила:
- Отвечай посетителю на текущем языке диалога.
- Поле "content" обязательно должно быть написано на этом языке.
- Отвечай кратко, вежливо и понятно.
- Не здоровайся с посетителем.
- Ты не должен впускать посетителя или отказывать ему во входе. Твоя задача - только выяснить цель визита.
- Если цель визита ещё не ясна, задай уточняющий вопрос.
- Если цель визита понятна, обязательно заполни поле 'visitor_goal'.
- Если посетитель пришёл не в IT компанию Эстэсис, а в другое место, тоже считай цель визита выясненной и устанавливай 'goal_identified' в true.
- Если похоже, что цель визита релевантна компании, но ты в этом не уверен (например: попасть на собеседование), то не считай цель выясненной - лучше задай уточняющий вопрос (например: вам назначено собеседование в Эстэсис?
- В таком случае в поле 'content' кратко объясни, что он, вероятнее всего, ошибся входом, и подскажи, что вход в бизнес-центр находится правее примерно в пятидесяти метрах.
- Все числа пиши словами.
- Верни только JSON без markdown и без дополнительных пояснений.

Поля ответа:
- content: текст ответа посетителю.
- visitor_goal: краткая формулировка цели визита; если цель ещё не ясна, верни null; Если ты установил goal_identified в true, то это поле обязательно должно быть заполнено; Текст в этом поле - всегда на русском языке, независимо от content.
- goal_identified: true, если цель визита уже понятна; если цель ещё не ясна, установи false.
"""

  GOAL_SCHEMA_PROMPT: ClassVar[str] = """
Верни строго JSON-объект следующего вида:
{
  "content": "string",
  "visitor_goal": "string | null",
  "goal_identified": false
}
Не добавляй никаких пояснений до или после JSON.
"""

  GRANT_ACCESS_INITIAL_PROMPT: ClassVar[str] = f"""
IT компания Эстэсис расположена в бизнес-центре. Компания не ждёт посетителей, цель визита которых - получить какие-либо услуги.

Ты получил кратко сформулированную цель визита посетителя. Твоя задача - определить, относится ли эта цель к компании Эстэсис.

Контекст:
- В компанию могут приходить сотрудники.
- Также могут приходить ожидаемые посетители: курьеры, доставка воды, еды, документов, техники, подрядчики, кандидаты на собеседование и другие приглашённые люди.
- Если цель визита связана с получением услуг, не относящихся к IT-компании, то такая цель не относится к компании Эстэсис.

Правила:
- Поле 'goal_relevant_to_company' означет: считаешь ли ты нужным предоставить посетителю доступ в компанию Estesis?
- Верни только JSON без markdown и без дополнительных пояснений.

Примеры целей, относящихся к компании:
- собеседование
- доставка воды
- доставка документов
- встреча с сотрудником
- пришёл на работу
- обслуживание техники
- подрядные работы

Примеры целей, не относящихся к компании:
- оформление кредита
- маникюр
- стрижка
- массаж
- визит в банк
- получение бытовых или салонных услуг

Поля ответа:
- goal_relevant_to_company: если посетитель пришёл именно в компанию Эстэсис и цель визита выглядит допустимой, установи goal_relevant_to_company в true; иначе false.
"""

  GRANT_ACCESS_SCHEMA_PROMPT: ClassVar[str] = """
Верни строго JSON-объект следующего вида:
{
  "goal_relevant_to_company": false
}
Не добавляй никаких пояснений до или после JSON.
"""

  WANT_TO_ENTER_INITIAL_PROMPT: ClassVar[str] = f"""
Пользователь отвечает на вопрос: '{BotMessageConst.get(BotMessageEnum.WANT_TO_ENTER_QUESTION, LanguageEnum.RU)}'.
Определи:
- want_to_enter = true, если ответ положительный (то есть человек настаивает на входе в компанию),
- want_to_enter = false, если человек отказывается от входа, уходит или по смыслу не хочет продолжать попытку входа.

Примеры положительных ответов:
- 'да'
- 'впустите меня'
- 'открывайте'
- 'само собой'
- 'я всё равно зайду'
- 'да, впускайте'
- 'у меня запись, впускайте меня'
- 'вызовите сотрудника'
- 'я хочу войти'

Примеры отрицательных ответов:
- 'нет'
- 'не надо'
- 'да не надо'
- 'да нет'
- 'не хочу'
- 'ладно, я пойду'
- 'всё, тогда не нужно'

Верни только JSON без markdown и без дополнительных пояснений.

Поля ответа:
- want_to_enter: true, если пользователь подтверждает вход; false - если отказывается или ответ не выражает согласия на вход.
"""

  WANT_TO_ENTER_SCHEMA_PROMPT: ClassVar[str] = """
Верни строго JSON-объект с полями:
- want_to_enter: boolean

Примеры валидных ответов:
{
  "want_to_enter": true
}

{
  "want_to_enter": false
}

Не добавляй никаких пояснений до или после JSON.
"""
  

class DialogueConfigConst:
  MODE_CONFIG_MAP: ClassVar[dict[DialogueModeEnum, DialogueConfig]] = {
      # Stage 0
      DialogueModeEnum.DETECT_LANGUAGE: DialogueConfig(
          initial_prompt = PromptConst.DETECT_LANGUAGE_INITIAL_PROMPT,
          bot_answer_schema_prompt = PromptConst.DETECT_LANGUAGE_SCHEMA_PROMPT,
          bot_answer_schema = DetectLanguageBotAnswer,
      ),
      # Stage 1
      DialogueModeEnum.VISITOR_CALL_EMPLOYEE: DialogueConfig(
          initial_prompt = PromptConst.CALL_EMPLOYEE_INITIAL_PROMPT,
          bot_answer_schema_prompt = PromptConst.CALL_EMPLOYEE_SCHEMA_PROMPT,
          bot_answer_schema = VisitorCallEmployeeBotAnswer,
      ),
      # Stage 2
      DialogueModeEnum.GOAL: DialogueConfig(
          initial_prompt = PromptConst.GOAL_INITIAL_PROMPT,
          bot_answer_schema_prompt = PromptConst.GOAL_SCHEMA_PROMPT,
          bot_answer_schema = GoalDialogueBotAnswer,
      ),
      # Stage 3
      DialogueModeEnum.GRANT_ACCESS: DialogueConfig(
          initial_prompt = PromptConst.GRANT_ACCESS_INITIAL_PROMPT,
          bot_answer_schema_prompt = PromptConst.GRANT_ACCESS_SCHEMA_PROMPT,
          bot_answer_schema = GrantAccessDialogueBotAnswer,
      ),
      # Stage 4
      DialogueModeEnum.WANT_TO_ENTER: DialogueConfig(
          initial_prompt = PromptConst.WANT_TO_ENTER_INITIAL_PROMPT,
          bot_answer_schema_prompt = PromptConst.WANT_TO_ENTER_SCHEMA_PROMPT,
          bot_answer_schema = WantToEnterBotAnswer,
      ),
  }

class DialogueConsts:
  def __init__(self):
    self.Prompt = PromptConst
    self.Message = BotMessageConst
    self.DialogueConfig = DialogueConfigConst
