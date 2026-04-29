from app.sensitivity_checker import rule_based_detection
from app.ml_model import predict

HIGH_CONFIDENCE = 0.75
LOW_CONFIDENCE  = 0.40

def route_message(text):
    #Run multi-rule checker
    rule_result = rule_based_detection(text)

    if rule_result["sensitive"]:
        return {
            "route": "LOCAL",
            "reason": rule_result["reason"],
            "rules_triggered": rule_result["rules_triggered"],
            "rule_count": rule_result["rule_count"]
        }

    #ML probability
    probability = predict(text)

    if probability >= HIGH_CONFIDENCE:
        return {
            "route": "LOCAL",
            "reason": f"ML high confidence sensitive ({probability:.2f})",
            "rules_triggered": [],
            "rule_count": 0
        }
    elif probability <= LOW_CONFIDENCE:
        return {
            "route": "CLOUD",
            "reason": f"ML high confidence safe ({probability:.2f})",
            "rules_triggered": [],
            "rule_count": 0
        }
    else:
        return {
            "route": "LOCAL",
            "reason": f"Uncertain probability ({probability:.2f}), default LOCAL",
            "rules_triggered": [],
            "rule_count": 0
        }
