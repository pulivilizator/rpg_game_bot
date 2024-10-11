from pathlib import Path

from fluent_compiler.bundle import FluentBundle

from fluentogram import FluentTranslator, TranslatorHub

BASE_DIR = Path(__file__).parent.parent.parent

def create_translator_hub() -> TranslatorHub:
    translator_hub = TranslatorHub(
        {
            "ru": ("ru", "en"),
            "en": ("en", "ru")
        },
        [
            FluentTranslator(
                locale="ru",
                translator=FluentBundle.from_files(
                    locale="ru-RU",
                    filenames=[BASE_DIR / 'locales' / 'ru' / 'LC_MESSAGES' / 'txt.ftl'])),
            FluentTranslator(
                locale="en",
                translator=FluentBundle.from_files(
                    locale="en-US",
                    filenames=[BASE_DIR / 'locales' / 'en' / 'LC_MESSAGES' / 'txt.ftl']))
        ],
    )
    return translator_hub