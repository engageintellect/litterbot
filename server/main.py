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
    return [str(robot) for robot in account.robots]

@app.get("/api/dump")
async def get_dump():
    return account.robots[0].__dict__

@app.get("/api/activity")
async def get_activity():
    return await account.robots[0].get_activity_history()

@app.get("/api/status")
async def get_status():
    return account.robots[0].__dict__['_data']['robotStatus']

@app.get("/api/clean")
async def start_cleaning():
    await account.robots[0].start_cleaning()
    status = account.robots[0].__dict__['_data']['robotStatus']
    return {"msg": "Cleaning started...", "robot": str(account.robots[0]), "status": status}

@app.get("/api/lightOn")
async def light_on():
    return await account.robots[0].set_night_light(True)

@app.get("/api/lightOff")
async def light_off():
    return await account.robots[0].set_night_light(False)


@app.websocket("/api/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print(f"WebSocket connection established with: {websocket.client}")
    try:
        while True:
            # Refresh or reconnect account to ensure fresh data
            await disconnect_account()  # Ensure it's disconnected first to avoid issues
            await connect_account()  # Reconnect to fetch fresh data
            
            # Serialize robots data
            robots_data = [{key: str(value) for key, value in robot.__dict__.items()} for robot in account.robots]
            
            # Serialize dump data; assuming robots[0] exists and checking its data type before serializing
            dump_data = {}
            if account.robots:
                robot = account.robots[0]
                for key, value in robot.__dict__.items():
                    if isinstance(value, (dict, list, str, int, float, bool, type(None))):
                        dump_data[key] = value
                    else:
                        dump_data[key] = str(value)

            # Assuming status is already being sent properly as a simpler dict or string
            status_data = account.robots[0].__dict__['_data']['robotStatus'] if account.robots else {}

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
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=4323, reload=True)
