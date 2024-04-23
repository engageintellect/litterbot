from fastapi import FastAPI, HTTPException
import os
from dotenv import load_dotenv
from pylitterbot import Account
import uvicorn


load_dotenv()

app = FastAPI()

username = os.getenv("LITTERBOT_USERNAME")
password = os.getenv("LITTERBOT_PASSWORD")
repository = "https://github.com/engageintellect/whisker"


def get_account():
    account = Account()
    return account

async def account_operation(operation):
    account = get_account()
    try:
        await account.connect(username=username, password=password, load_robots=True)
        return await operation(account)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await account.disconnect()

@app.get("/")
async def get_root():
    return {
        "msg": "hello world!", 
        "app": "litterbot", 
        "version": "0.0.2", 
        "repository": repository}    

@app.get("/api/refresh")
async def get_refresh():
    async def operation(account):
        return await account.robots[0].refresh()
    return await account_operation(operation)

@app.get("/api/robots")
async def get_robot_details():
    async def operation(account):
        return [str(robot) for robot in account.robots]
    return await account_operation(operation)

@app.get("/api/dump")
async def get_all():
    async def operation(account):
        return account.robots[0].__dict__
    return await account_operation(operation)

@app.get("/api/activity")
async def get_activity():
    async def operation(account):
        return await account.robots[0].get_activity_history()
    return await account_operation(operation)

@app.get("/api/status")
async def get_status():
    async def operation(account):
        return account.robots[0].__dict__['_data']['robotStatus']
    return await account_operation(operation)

@app.get("/api/clean")
async def start_cleaning():
    async def operation(account):
        await account.robots[0].start_cleaning()
        status = account.robots[0].__dict__['_data']['robotStatus']
        return {"msg": "Cleaning started...", "robot": str(account.robots[0]), "status": status}
    return await account_operation(operation)

@app.get("/api/lightOn")
async def light_on():
    async def operation(account):
        return await account.robots[0].set_night_light(True)
    return await account_operation(operation)

@app.get("/api/lightOff")
async def light_off():
    async def operation(account):
        return await account.robots[0].set_night_light(False)
    return await account_operation(operation)

# Main entry point for running the application directly
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=9009, reload=True)
