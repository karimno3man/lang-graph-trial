from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
from agent import app as agent_app
import uvicorn

server = FastAPI()

server.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static frontend
server.mount("/static", StaticFiles(directory="static"), name="static")

class ChatRequest(BaseModel):
    message: str
    thread_id: str  # unique per conversation session

@server.get("/")
def root():
    return FileResponse("static/index.html")

@server.post("/chat")
async def chat(req: ChatRequest):
    config = {"configurable": {"thread_id": req.thread_id}}

    result = agent_app.invoke(
        {
            "messages": [HumanMessage(content=req.message)],
            "persona": ""
        },
        config=config
    )

    last_message = result["messages"][-1]
    persona = result["persona"]

    persona_labels = {
        "cfo": "CFO",
        "cto": "CTO",
        "sales": "Business Dev / GTM / Sales"
    }

    return {
        "reply": last_message.content,
        "persona": persona,
        "persona_label": persona_labels.get(persona, "Assistant")
    }

if __name__ == "__main__":
    uvicorn.run("server:server", host="0.0.0.0", port=8000, reload=True)
