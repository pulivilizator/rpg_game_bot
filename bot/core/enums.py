from enum import StrEnum, IntEnum


class BaseKeys(StrEnum):
    WIDGET_KEY: str
    REDIS_KEY: str

class UserKeys(StrEnum):
    USER_KEY = 'user:{}'

class LanguageList(StrEnum):
    RU = 'ru'
    EN = 'en'

class Language(BaseKeys):
    DEFAULT = LanguageList.RU

    WIDGET_KEY = 'language'
    REDIS_KEY = 'language'

class LinksRedisKeys(StrEnum):
    PERSONAL_CABINET = 'personal_cabinet'
    LAUNCHER_YANDEX_DISC = 'launcher:yandex_disc'
    LAUNCHER_GOOGLE_DRIVE = 'launcher:google_drive'
    PHOTO = 'photo'
    PROMO_CODES = 'promo_codes'
    USER_PROMO_USED = 'user_promo_used:{}'

class MailingKeys(StrEnum):
    TEXT = 'mailing:text'
    MEDIA = 'mailing:media'
    LINKS = 'mailing:links'

    SUBJECT = 'mailing'
    STREAM = 'mailing_stream'
    DURABLE_NAME = 'mailing_durable'

    EX_TEXT_TIME = '604800'