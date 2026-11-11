import re
from typing import Optional

def redact_email(text: str) -> str:
    # A robust regex for emails. Matches common patterns.
    # Exclude trailing period from match to fix punctuation issue.
    # We use a standard regex matching the basic format of an email
    email_regex = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+[a-zA-Z0-9-]'
    return re.sub(email_regex, '[REDACTED_EMAIL_GDPR]', text)

def redact_phone(text: str) -> str:
    def replacer(match):
        m = match.group(0)
        digit_count = sum(c.isdigit() for c in m)
        if 7 <= digit_count <= 15:
            return '[REDACTED_PHONE_GDPR]'
        return m

    # Find sequences of digits, spaces, pluses, dashes, dots, and parens
    # that are separated from surrounding text.
    broad_phone_regex = r'(?:\+?[0-9][0-9 \-\.\(\)]{5,20}[0-9])'

    return re.sub(broad_phone_regex, replacer, text)


def redact_iban(text: str) -> str:
    iban_regex = r'\b[A-Z]{2}[0-9]{2}(?:[ ]?[A-Z0-9]){11,30}\b'
    return re.sub(iban_regex, '[REDACTED_IBAN_GDPR]', text)

def check_prompt_injection(text: str) -> bool:
    """Returns True if prompt injection is suspected."""
    injection_patterns = [
        r"ignore previous instructions",
        r"ignore all previous instructions",
        r"disregard previous instructions",
        r"you are now (?:a|an)",
        r"system prompt",
        r"forget (?:all )?previous instructions",
        r"new instructions:",
        r"bypass safety",
        r"jailbreak"
    ]

    for pattern in injection_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False

def verify_and_sanitize_input(text: Optional[str]) -> Optional[str]:
    if not text:
        return text

    if check_prompt_injection(text):
        return "[PROMPT_INJECTION_DETECTED]"

    sanitized = text
    sanitized = redact_iban(sanitized)
    sanitized = redact_email(sanitized)
    sanitized = redact_phone(sanitized)

    return sanitized
