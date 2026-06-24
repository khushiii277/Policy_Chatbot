from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from langchain_core.messages import HumanMessage
from src.graph import app_graph

app = FastAPI(title="Corporate Policy Chatbot")

# --- NEW: Route to serve your index.html ---
@app.get("/")
async def get_frontend():
    # Tell FastAPI exactly where the HTML file is located
    return FileResponse("public/index.html")
# -------------------------------------------

@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    state = {"messages": [], "context": ""}
    
    try:
        while True:
            user_text = await websocket.receive_text()
            state["messages"].append(HumanMessage(content=user_text))
            await websocket.send_text("SYSTEM: Searching policies...")
            
            result = app_graph.invoke(state)
            
            ai_message = result["messages"][-1]
            state["messages"] = result["messages"] 
            
            await websocket.send_text(f"BOT: {ai_message.content}")
            
    except WebSocketDisconnect:
        print("User WebSocket connection closed.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)