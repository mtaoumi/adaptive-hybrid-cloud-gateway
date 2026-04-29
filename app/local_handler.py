import httpx

OLLAMA_URL   = "http://localhost:11434/api/chat"
OLLAMA_MODEL = "qwen2:0.5b"

def send_to_local_ai(message: str) -> str:
    for attempt in range(2):
        try:
            response = httpx.post(
                OLLAMA_URL,
                json={
                    "model": OLLAMA_MODEL,
                    "messages": [{"role": "user", "content": message}],
                    "stream": False,
                    "options": {"num_predict": 200}
                },
                timeout=None
            )
            result = response.json()
            if "message" in result:
                return result["message"]["content"]
            elif "response" in result:
                return result["response"]
            return f"Unexpected response: {result}"
        except Exception as e:
            if attempt == 0:
                continue
            return f"Local AI error: {str(e)}"
    return "Local AI error: failed after retry"
