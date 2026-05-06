import asyncio
import socket
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from typing import List

app = FastAPI()

app.mount("/static", StaticFiles(directory="templates"), name="static")

# Configuration
UDP_IP = "127.0.0.1"
UDP_PORT = 5005

# Store active WebSocket connections
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

# UDP Listener Task
async def udp_listener():
    # Create a non-blocking UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))
    sock.setblocking(False)
    
    print(f"UDP Listener started on {UDP_IP}:{UDP_PORT}")
    
    loop = asyncio.get_event_loop()
    while True:
        # Receive data using the event loop to avoid blocking
        data, addr = await loop.sock_recvfrom(sock, 1024)
        message = data.decode('utf-8')
        print(f"Received from {addr}: {message}")
        
        # Send to all connected web browsers
        await manager.broadcast(message)

@app.on_event("startup")
async def startup_event():
    # Start the UDP listener as a background task
    asyncio.create_task(udp_listener())

@app.get("/")
async def get():
    with open("templates/index.html", "r") as f:
        return HTMLResponse(content=f.read())

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Keep connection alive
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)