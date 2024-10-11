from typing import Literal

    
class TranslatorRunner:
    def get(self, path: str, **kwargs) -> str: ...
    
    launcher: Launcher
    download_from: Download_from
    idea_bot: Idea_bot
    promo_code: Promo_code
    discord: Discord
    lang: Lang
    admin_menu: Admin_menu
    setup_launcher_links: Setup_launcher_links
    setup_image: Setup_image
    setup_personal_cabinet_link: Setup_personal_cabinet_link
    yandex_disc: Yandex_disc
    google_drive: Google_drive
    setup_promo_codes: Setup_promo_codes
    mailing: Mailing
    incorrect: Incorrect

    @staticmethod
    def menu_message() -> Literal["""Main menu"""]: ...

    @staticmethod
    def personal_cabinet_button() -> Literal["""Personal Cabinet 🏛"""]: ...

    @staticmethod
    def admin_menu_button() -> Literal["""Administration"""]: ...

    @staticmethod
    def change_lang_button() -> Literal["""Change language"""]: ...

    @staticmethod
    def subscribe_button() -> Literal["""Subscribe"""]: ...

    @staticmethod
    def subscribe_check_button() -> Literal["""Check"""]: ...

    @staticmethod
    def previous_button() -> Literal["""Back"""]: ...

    @staticmethod
    def next_button() -> Literal["""Next"""]: ...

    @staticmethod
    def skip_button() -> Literal["""Skip"""]: ...


class Launcher:
    @staticmethod
    def button() -> Literal["""Download Updater 📦"""]: ...

    @staticmethod
    def message() -> Literal["""Choose where to download from"""]: ...

    @staticmethod
    def empty_message() -> Literal["""No links found"""]: ...


class Download_from:
    yandex: Download_fromYandex
    google: Download_fromGoogle


class Download_fromYandex:
    @staticmethod
    def button() -> Literal["""Yandex Disc"""]: ...


class Download_fromGoogle:
    @staticmethod
    def button() -> Literal["""Google Drive"""]: ...


class Idea_bot:
    @staticmethod
    def button() -> Literal["""Suggest Idea 💡"""]: ...


class Promo_code:
    @staticmethod
    def button() -> Literal["""Free Pre-Start Box 🎁"""]: ...

    @staticmethod
    def message(*, code) -> Literal["""Your promo code: &lt;code&gt;{ $code }&lt;/code&gt;"""]: ...

    @staticmethod
    def subscribe() -> Literal["""Subscribe to the channel first:"""]: ...

    @staticmethod
    def used_message(*, code) -> Literal["""You have already received a promo code:
&lt;code&gt;{ $code }&lt;/code&gt;"""]: ...

    @staticmethod
    def empty_message() -> Literal["""Promo codes expired"""]: ...


class Discord:
    @staticmethod
    def button() -> Literal["""Hello Kitty x Razer and a gift in Discord  🎀"""]: ...


class Lang:
    @staticmethod
    def russian() -> Literal["""Русский 🇷🇺"""]: ...

    @staticmethod
    def english() -> Literal["""English 🇬🇧"""]: ...


class Admin_menu:
    @staticmethod
    def message(*, users_count, promo_codes_count) -> Literal["""Admin Menu

Current number of users: { $users_count }
Number of unused promo codes: { $promo_codes_count }"""]: ...


class Setup_launcher_links:
    @staticmethod
    def button() -> Literal["""Set links to download the launcher."""]: ...

    @staticmethod
    def message() -> Literal["""Set up links to download launcher"""]: ...


class Setup_image:
    @staticmethod
    def button() -> Literal["""Set up an image"""]: ...

    @staticmethod
    def message() -> Literal["""Set image"""]: ...


class Setup_personal_cabinet_link:
    @staticmethod
    def button() -> Literal["""Set link to personal cabinet"""]: ...

    @staticmethod
    def message() -> Literal["""Send link to personal account"""]: ...


class Yandex_disc:
    @staticmethod
    def button() -> Literal["""Yandex Disk"""]: ...

    @staticmethod
    def message() -> Literal["""Send link to Yandex Disk"""]: ...


class Google_drive:
    @staticmethod
    def button() -> Literal["""Google Drive"""]: ...

    @staticmethod
    def message() -> Literal["""Send link to Google Drive"""]: ...


class Setup_promo_codes:
    @staticmethod
    def button() -> Literal["""Send new promo codes"""]: ...

    @staticmethod
    def message() -> Literal["""Send a file with new promo codes"""]: ...


class Mailing:
    save_text: MailingSave_text
    save_media: MailingSave_media
    save_links: MailingSave_links
    start: MailingStart

    @staticmethod
    def button() -> Literal["""Start mailing"""]: ...


class MailingSave_text:
    @staticmethod
    def message() -> Literal["""Send a test message to be used in the newsletter"""]: ...


class MailingSave_media:
    @staticmethod
    def message() -> Literal["""Send a media file to be used in the newsletter."""]: ...


class MailingSave_links:
    @staticmethod
    def message() -> Literal["""Edit text and links for buttons separated by spaces in the format:
&lt;b&gt;Button 1 text https://example1.com
Button text 2 https://example2.com
Button text 3 https://example3.com&lt;/b&gt;"""]: ...


class MailingStart:
    @staticmethod
    def message() -> Literal["""Start mailing"""]: ...


class Incorrect:
    link: IncorrectLink
    photo: IncorrectPhoto


class IncorrectLink:
    @staticmethod
    def message() -> Literal["""Send correct link"""]: ...


class IncorrectPhoto:
    @staticmethod
    def message() -> Literal["""Отправьте корректную image"""]: ...

