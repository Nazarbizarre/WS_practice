from fastapi import FastAPI, WebSocket, WebSocketDisconnect, WebSocketException
from uvicorn import run as run_project

from ws import manager

app = FastAPI()
        
        
@app.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str, username: str):
    await manager.connect(websocket, room_id)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"{username} writes: {data}", room_id)
    except WebSocketDisconnect:
        manager.disconnect(websocket, room_id)
        await manager.broadcast(f"{username} left the chat", room_id)




if __name__ == "__main__":
    run_project(app=app)