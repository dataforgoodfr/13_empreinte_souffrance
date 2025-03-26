import gettext
from functools import lru_cache
from pathlib import Path
from typing import Callable


class I18N:
    def __init__(self):
        self.default_locale = "en"
        self.supported_locales = ["fr", "en"]
        self.locales_dir = Path(__file__).parent.parent / "locales"
        self.translations = {}
        self.load_translations()

    def get_supported_locales(self):
        return self.supported_locales

    def load_translations(self):
        """Load (or reload) translations for all supported locales"""
        self.translations.clear()
        for locale_dir in self.locales_dir.iterdir():
            if locale_dir.is_dir():
                locale = locale_dir.name
                translations = gettext.translation("messages", localedir=str(self.locales_dir), languages=[locale])
                self.translations[locale] = translations

    def get_translator(self, locale: str) -> Callable:
        """Get the gettext translator for the given locale"""
        if locale in self.translations:
            return self.translations[locale].gettext
        return self.translations[self.default_locale].gettext

    def is_supported_locale(self, locale: str) -> bool:
        """Check if the given locale is supported"""
        return locale in self.supported_locales

    def reload(self):
        """Reload translations and clear the cache"""
        self.load_translations()
        get_i18n.cache_clear()


@lru_cache()
def get_i18n():
    return I18N()
