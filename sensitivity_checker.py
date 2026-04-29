import re

SENSITIVE_KEYWORDS = [
    "salary", "confidential", "internal", "bank account",
    "credit card", "id number", "ssn", "password",
    "medical record", "classified", "personal data", "payroll",
    "login credentials", "secret", "private", "account number",
    "pin code", "passport", "national id", "date of birth"
]

def contains_sensitive_keyword(text):
    text_lower = text.lower()
    found = []
    for word in SENSITIVE_KEYWORDS:
        if word in text_lower:
            found.append(f"keyword '{word}'")
    return found

def contains_email(text):
    matches = re.findall(
        r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
        text
    )
    if matches:
        return [f"email address detected ({matches[0]})"]
    return []

def contains_numbers_pattern(text):
    matches = re.findall(r"\b\d{5,}\b", text)
    if matches:
        return [f"sensitive number pattern detected ({matches[0]})"]
    return []

def contains_personal_pronoun_with_sensitive(text):
    text_lower = text.lower()
    personal_pronouns = ["my ", "our ", "his ", "her ", "their "]
    found = []
    for pronoun in personal_pronouns:
        if pronoun in text_lower:
            for word in SENSITIVE_KEYWORDS:
                if word in text_lower:
                    found.append(
                        f"personal pronoun '{pronoun.strip()}' "
                        f"used with sensitive keyword '{word}'"
                    )
    return found

def rule_based_detection(text):
    """
    Returns a dict with:
      - sensitive: True/False
      - rules_triggered: list of all rules that fired
      - rule_count: number of rules triggered
      - reason: human-readable summary
    """
    all_triggers = []

    all_triggers += contains_sensitive_keyword(text)
    all_triggers += contains_email(text)
    all_triggers += contains_numbers_pattern(text)
    all_triggers += contains_personal_pronoun_with_sensitive(text)

    # Remove duplicates while preserving order
    seen = set()
    unique_triggers = []
    for t in all_triggers:
        if t not in seen:
            seen.add(t)
            unique_triggers.append(t)

    is_sensitive = len(unique_triggers) > 0

    if not is_sensitive:
        reason = "No sensitive patterns detected"
    elif len(unique_triggers) == 1:
        reason = f"1 rule triggered: {unique_triggers[0]}"
    else:
        reason = (
            f"{len(unique_triggers)} rules triggered: "
            + " | ".join(unique_triggers)
        )

    return {
        "sensitive": is_sensitive,
        "rules_triggered": unique_triggers,
        "rule_count": len(unique_triggers),
        "reason": reason
    }