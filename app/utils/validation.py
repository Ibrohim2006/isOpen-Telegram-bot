import re
import phonenumbers


def validate_full_name(full_name: str) -> str:
    pattern = r"^[a-zA-Zа-яА-ЯёЁ\s]+$"
    full_name = full_name.strip()
    if not re.match(pattern, full_name):
        raise ValueError("Full name must contain only letters from the Latin or Cyrillic alphabet.")
    return full_name


def validate_phone_number(value: str) -> str:
    try:
        parsed = phonenumbers.parse(value, None)

        if not phonenumbers.is_valid_number(parsed):
            raise ValueError("Invalid phone number.")

        if parsed.country_code not in phonenumbers.COUNTRY_CODE_TO_REGION_CODE:
            raise ValueError("Unsupported country code in phone number.")

        return value

    except phonenumbers.NumberParseException:
        raise ValueError("Invalid phone number format.")


def validate_telegram_username(username: str) -> str:
    pattern = r"^@[\w\d_]{5,32}$"
    username = username.strip()
    if not re.match(pattern, username):
        raise ValueError("Telegram username must start with @ and be 5 to 32 characters long.")
    return username
