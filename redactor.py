import re
from app.sensitivity_checker import rule_based_detection

def split_into_fragments(text):
    sentences = re.split(r'(?<=[.!?])\s+|(?<=,)\s+', text)
    return [s.strip() for s in sentences if s.strip()]

def redact_sensitive_fragments(text):
    fragments = split_into_fragments(text)
    
    sensitive_parts = []
    safe_parts = []
    
    for fragment in fragments:
        result = rule_based_detection(fragment)
        if result["sensitive"]:
            sensitive_parts.append({
                "text": fragment,
                "rules": result["rules_triggered"]
            })
        else:
            safe_parts.append(fragment)
    
    safe_text = " ".join(safe_parts).strip()
    
    return {
        "original": text,
        "sensitive_parts": sensitive_parts,
        "safe_text": safe_text,
        "has_sensitive": len(sensitive_parts) > 0,
        "has_safe": len(safe_parts) > 0,
        "is_mixed": len(sensitive_parts) > 0 and len(safe_parts) > 0
    }
