from fastapi import FastAPI, WebSocket, WebSocketDisconnect




class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[int, list[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, room_id: int):
        await websocket.accept()
        self.active_connections.get(room_id).append(websocket)

    def disconnect(self, websocket: WebSocket, room_id:int):
        self.active_connections.get(room_id).remove(websocket)

    async def broadcast(self, message: str, room_id: int):
        for connection in self.active_connections.get(room_id):
            await connection.send_json(message)
            
    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_json(message)


manager = ConnectionManager()




