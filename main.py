import time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional
from app.router_logic import route_message
from app.logger import log_routing
from app.cloud_handler import send_to_cloud_ai
from app.local_handler import send_to_local_ai
from app.redactor import redact_sensitive_fragments

app = FastAPI(title="Adaptive Hybrid Cloud Gateway")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

class HistoryItem(BaseModel):
    role: str
    content: str

class MessageRequest(BaseModel):
    message: str
    history: Optional[List[HistoryItem]] = []

@app.get("/")
def home():
    return FileResponse("static/index.html")

@app.post("/chat")
def chat(request: MessageRequest):
    start_time = time.time()

    # Build context from history
    history_context = ""
    if request.history:
        for item in request.history[-6:]:
            role = "User" if item.role == "user" else "Assistant"
            history_context += f"{role}: {item.content}\n"
        history_context += "\n"

    full_message = history_context + request.message if history_context else request.message

    redaction = redact_sensitive_fragments(request.message)

    if redaction["has_sensitive"] and not redaction["has_safe"]:
        route = "LOCAL"
        reason = "All content is sensitive — processed locally"
        response_text = send_to_local_ai(full_message)
        local_response = response_text
        cloud_response = None

    elif redaction["is_mixed"]:
        route = "MIXED"
        reason = (
            f"{len(redaction['sensitive_parts'])} sensitive fragment(s) "
            f"kept local — safe part sent to cloud"
        )
        sensitive_text = history_context + " ".join(
            p["text"] for p in redaction["sensitive_parts"]
        )
        local_response = send_to_local_ai(sensitive_text)
        cloud_response = send_to_cloud_ai(
            history_context + redaction["safe_text"]
        )
        response_text = (
            f"[LOCAL — private data handled on-premises]\n{local_response}"
            f"\n\n[CLOUD — safe content]\n{cloud_response}"
        )

    else:
        routing_result = route_message(request.message)
        route = routing_result["route"]
        reason = routing_result["reason"]
        if route == "LOCAL":
            response_text = send_to_local_ai(full_message)
            local_response = response_text
            cloud_response = None
        else:
            response_text = send_to_cloud_ai(full_message)
            local_response = None
            cloud_response = response_text

    processing_time = round(time.time() - start_time, 4)
    log_routing(request.message, route, reason)

    return {
        "input":                   request.message,
        "route":                   route,
        "reason":                  reason,
        "sensitive_fragments":     redaction["sensitive_parts"],
        "safe_text_sent_to_cloud": redaction["safe_text"] if redaction["is_mixed"] else None,
        "response":                response_text,
        "processing_time_seconds": processing_time
    }

@app.get("/health")
def health():
    return {"status": "gateway running"}