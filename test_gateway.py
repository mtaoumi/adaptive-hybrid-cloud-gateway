import requests

url = "http://127.0.0.1:8000/chat"

test_messages = [
    "My salary is 5000 dollars",
    "Send me the internal financial report",
    "My email is maryam@example.com",
    "Explain machine learning",
    "Write a poem about AI",
    "What is cloud computing",
    "My bank account number is 123456789",
    "Tell me a joke"
]

for msg in test_messages:

    response = requests.post(
        url,
        json={"message": msg}
    )

    result = response.json()

    print("Message:", msg)
    print("Route:", result["route"])
    print("Reason:", result["reason"])
    print("------------")
