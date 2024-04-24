#!/usr/bin/env python3
from fastapi import FastAPI, WebSocket, HTTPException
import subprocess
import uvicorn
import asyncio
from dotenv import load_dotenv
from pylitterbot import Account
import os


load_dotenv()

app = FastAPI()

username = os.getenv("LITTERBOT_USERNAME")
password = os.getenv("LITTERBOT_PASSWORD")
repository = "https://github.com/engageintellect/whisker"

# Global variable for the account to maintain persistent connection
account = None

async def connect_account():
    global account
    account = Account()
    await account.connect(username=username, password=password, load_robots=True)

async def disconnect_account():
    global account
    if account:
        await account.disconnect()
        account = None

@app.on_event("startup")
async def startup_event():
    await connect_account()

@app.on_event("shutdown")
async def shutdown_event():
    await disconnect_account()

@app.get("/")
async def get_root():
    return {"msg": "hello world!", "app": "litterbot", "version": "0.0.2", "repository": repository}

@app.get("/api/refresh")
async def get_refresh():
    return await account.robots[0].refresh()

@app.get("/api/robots")
async def get_robots():
    if not await account.robots:
        return {"error": "No robots available"}
    return [str(robot) for robot in account.robots]

@app.get("/api/dump")
async def get_dump():
    if not account.robots:
        raise HTTPException(status_code=404, detail="No robots available")
    return account.robots[0].__dict__

@app.get("/api/activity")
async def get_activity():
    if not account.robots:
        raise HTTPException(status_code=404, detail="No robots available")
    return await account.robots[0].get_activity_history()

@app.get("/api/status")
async def get_status():
    if not account.robots:
        raise HTTPException(status_code=404, detail="No robots available")
    return account.robots[0].__dict__['_data']['robotStatus']

@app.get("/api/clean")
async def start_cleaning():
    if not account.robots:
        raise HTTPException(status_code=404, detail="No robots available")
    await account.robots[0].start_cleaning()
    status = account.robots[0].__dict__['_data']['robotStatus']
    return {"msg": "Cleaning started...", "robot": str(account.robots[0]), "status": status}

@app.get("/api/lightOn")
async def light_on():
    if not account.robots:
        raise HTTPException(status_code=404, detail="No robots available")
    return await account.robots[0].set_night_light(True)

@app.get("/api/lightOff")
async def light_off():
    if not account.robots:
        raise HTTPException(status_code=404, detail="No robots available")
    return await account.robots[0].set_night_light(False)

# Adjusting the WebSocket endpoint to handle multiple robots
@app.websocket("/api/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print(f"WebSocket connection established with: {websocket.client}")
    try:
        while True:
            await disconnect_account()  # Ensure it's disconnected first to avoid issues
            await connect_account()  # Reconnect to fetch fresh data
            
            if not account.robots:
                await websocket.send_json({"error": "No robots available"})
            else:
                robots_data = [{key: str(value) for key, value in robot.__dict__.items()} for robot in account.robots]
                robot = account.robots[0]  # Using the first robot for detailed data
                dump_data = {key: (value if isinstance(value, (dict, list, str, int, float, bool, type(None))) else str(value)) for key, value in robot.__dict__.items()}
                status_data = robot.__dict__['_data']['robotStatus']
                
                data = {
                    "robots": robots_data,
                    "dump": dump_data,
                    "status": status_data,
                }
                await websocket.send_json(data)
            await asyncio.sleep(5)  # Send updated data every 5 seconds
    except Exception as e:
        print(f"WebSocket connection error: {e}")
    finally:
        print(f"WebSocket connection closed with: {websocket.client}")


# Main entry point for running the application directly
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=4323, reload=True)
