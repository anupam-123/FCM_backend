from typing import Annotated
from fastapi import FastAPI
from firebase_admin import messaging, credentials, initialize_app, _apps
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DeviceToken:
    token: str
    title: str
    body: str

@app.post("/test/{device_token}")
async def root(device_token: Annotated[str, "Unique Token of each device"]):
    cred = credentials.Certificate("./fir-auth-41b55-firebase-adminsdk-p6cud-cc179c8814.json")
    if not _apps:
        cred = credentials.Certificate("./fir-auth-41b55-firebase-adminsdk-p6cud-cc179c8814.json")
        initialize_app(cred)    
    json_data: DeviceToken = json.loads(device_token)
    message = messaging.Message(notification=messaging.Notification(title=json_data['title'], body=json_data['body']), token=json_data['token'])
    try:
        response = messaging.send(message)
        print(response)
        return {"message": response}
    except Exception as e:
        print("Error sending message",e)
