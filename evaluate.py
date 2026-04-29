import requests
import time
import json
from datetime import datetime

URL = "http://127.0.0.1:8000/chat"

TEST_CASES = [
    {"message": "My salary is 5000 dollars",                     "expected": "LOCAL"},
    {"message": "My email is john@example.com",                  "expected": "LOCAL"},
    {"message": "My bank account number is 123456789",           "expected": "LOCAL"},
    {"message": "Send me the internal financial report",         "expected": "LOCAL"},
    {"message": "My password is secret123",                      "expected": "LOCAL"},
    {"message": "This document is confidential",                 "expected": "LOCAL"},
    {"message": "My national ID is AB123456",                    "expected": "LOCAL"},
    {"message": "Patient medical record ID 78432",               "expected": "LOCAL"},
    {"message": "My credit card number is 4111111111111111",     "expected": "LOCAL"},
    {"message": "Employee payroll data for March 2026",          "expected": "LOCAL"},
    {"message": "Explain machine learning",                      "expected": "CLOUD"},
    {"message": "What is cloud computing?",                      "expected": "CLOUD"},
    {"message": "Write a short poem about AI",                   "expected": "CLOUD"},
    {"message": "What is an API?",                               "expected": "CLOUD"},
    {"message": "How does encryption work?",                     "expected": "CLOUD"},
    {"message": "Explain the difference between AI and ML",      "expected": "CLOUD"},
    {"message": "What is natural language processing?",          "expected": "CLOUD"},
    {"message": "How do recommendation systems work?",           "expected": "CLOUD"},
    {"message": "What is Python used for?",                      "expected": "CLOUD"},
    {"message": "Tell me about the history of computers",        "expected": "CLOUD"},
    {"message": "My salary is 5000. Explain machine learning.",  "expected": "MIXED"},
    {"message": "My email is a@b.com. What is cloud computing?", "expected": "MIXED"},
]

def run_evaluation():
    print("\n" + "="*60)
    print("   ADAPTIVE HYBRID CLOUD GATEWAY — EVALUATION REPORT")
    print(f"   Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)

    results = []
    local_latencies  = []
    cloud_latencies  = []
    mixed_latencies  = []

    correct   = 0
    fp        = 0  # false positive: safe sent LOCAL
    fn        = 0  # false negative: sensitive sent CLOUD
    errors    = 0

    print(f"\n{'#':<3} {'Message':<45} {'Expected':<8} {'Got':<8} {'OK?':<5} {'Time(s)'}")
    print("-"*90)

    for i, case in enumerate(TEST_CASES):
        msg      = case["message"]
        expected = case["expected"]

        try:
            start = time.time()
            resp  = requests.post(URL, json={"message": msg}, timeout=120)
            elapsed = round(time.time() - start, 2)
            data  = resp.json()
            actual = data.get("route", "ERROR")
        except Exception as e:
            actual  = "ERROR"
            elapsed = 0
            errors += 1

        is_correct = (actual == expected) or (
            expected == "MIXED" and actual == "MIXED"
        )

        if is_correct:
            correct += 1
            status = "YES"
        else:
            status = "NO"
            if expected == "CLOUD" and actual == "LOCAL":
                fp += 1  # false positive
            elif expected == "LOCAL" and actual == "CLOUD":
                fn += 1  # false negative — critical
        if actual == "LOCAL":
            local_latencies.append(elapsed)
        elif actual == "CLOUD":
            cloud_latencies.append(elapsed)
        elif actual == "MIXED":
            mixed_latencies.append(elapsed)

        results.append({
            "message":  msg,
            "expected": expected,
            "actual":   actual,
            "correct":  is_correct,
            "time":     elapsed
        })

        short_msg = msg[:44] + "…" if len(msg) > 44 else msg
        print(f"{i+1:<3} {short_msg:<45} {expected:<8} {actual:<8} {status:<5} {elapsed}")

    total     = len(TEST_CASES)
    accuracy  = round((correct / total) * 100, 1)
    fp_rate   = round((fp / total) * 100, 1)
    fn_rate   = round((fn / total) * 100, 1)

    avg_local  = round(sum(local_latencies)  / len(local_latencies),  2) if local_latencies  else 0
    avg_cloud  = round(sum(cloud_latencies)  / len(cloud_latencies),  2) if cloud_latencies  else 0
    avg_mixed  = round(sum(mixed_latencies)  / len(mixed_latencies),  2) if mixed_latencies  else 0

    print("\n" + "="*60)
    print("   RESULTS SUMMARY")
    print("="*60)
    print(f"   Total messages tested    : {total}")
    print(f"   Correctly routed         : {correct} / {total}  ({accuracy}%)")
    print(f"   False positives          : {fp}  ({fp_rate}%)  — safe msgs sent LOCAL")
    print(f"   False negatives          : {fn}  ({fn_rate}%)  — sensitive msgs sent CLOUD")
    print(f"   Errors                   : {errors}")
    print("-"*60)
    print(f"   Avg LOCAL latency        : {avg_local}s")
    print(f"   Avg CLOUD latency        : {avg_cloud}s")
    print(f"   Avg MIXED latency        : {avg_mixed}s")
    print("-"*60)

    if fn == 0:
        print("   PRIVACY STATUS: PASS — no sensitive data leaked to cloud")
    else:
        print(f"   PRIVACY STATUS: FAIL — {fn} sensitive message(s) sent to cloud")

    print("="*60)
    
    report = {
        "date":          datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "total":         total,
        "correct":       correct,
        "accuracy_pct":  accuracy,
        "false_positives": fp,
        "false_negatives": fn,
        "fp_rate_pct":   fp_rate,
        "fn_rate_pct":   fn_rate,
        "avg_local_latency_s":  avg_local,
        "avg_cloud_latency_s":  avg_cloud,
        "avg_mixed_latency_s":  avg_mixed,
        "results":       results
    }

    with open("logs/evaluation_report.json", "w") as f:
        json.dump(report, f, indent=2)

    print(f"\n   Full report saved to: logs/evaluation_report.json")
    print("="*60 + "\n")

if __name__ == "__main__":
    run_evaluation()
