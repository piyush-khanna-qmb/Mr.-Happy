from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request, HTTPException, Form, Query
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from pymongo.mongo_client import MongoClient

from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from fastapi.responses import RedirectResponse, HTMLResponse, StreamingResponse

from core.model import FirstLayerDMM
from core.rt import RealtimeSearchEngine
from core.general import GeneralChatBot
from core.voice import TextToSpeechBytes
from core.camgpt import ChatBotAI
from functions.wopen import wopen
from functions.content import Content

from utils.unsupported import playonyt
from utils.basic import UniversalTranslator, AnswerModifier, QueryModifier
from utils.notepaduri import create_content_url
from utils.guimessage import GuiMessagesConverter

import asyncio
import json
import base64
import io



user_db: dict[str, dict[str, str]] = {
    "Harry919289874598": {
        "Username": "Harry",
        "Age": "23",
        "Email": "ZsBmAYO2b5Zrrhgy@zoom.yc1345u.mongodb.net/?retryWrites=true&w=majority&appName=zoom",
        "ContactNumber": "919289874598",
        "Address": "Haryana",
        "Gender": "Male",
        "DOB": "01-01-2000",
        "Height": "5.11"
    }
}
message_db: dict[str, list[dict[str, str]]] = {
    "Harry919289874598": []
}
app = FastAPI()
# Add session middleware
app.add_middleware(SessionMiddleware, secret_key="your_secret_key")

# Setup templates
templates = Jinja2Templates(directory="web")


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse(
        "login.html",
        {
            "request": request
        }
    )

@app.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    user = user_db.get(username+password)
    if user:
        return templates.TemplateResponse("home.html", {"request": request, "UserName": username, "email": username, "password": password})
    raise HTTPException(status_code=400, detail="Incorrect username or password")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    auth0: dict = json.loads(
        await websocket.receive_text()
        )
    email = auth0["email"]
    password = auth0["password"]
    if (email + password) in user_db:
        user_details = user_db[email + password]
        Username = "Mr. Happy"
        await websocket.send_text("Authentication successful")
    else:
        await websocket.send_text("Authentication failed")
        return

    await websocket.send_text(json.dumps(
        {
            "display": GuiMessagesConverter(Username,user_db[email + password]["Username"],message_db[email + password])
        }
        ))
    dmm_history = []
    try:
        while True:
            
            data_json = (
                json.loads(await websocket.receive_text())
                )
            Query = data_json["query"].capitalize()
            print(Query)
            Image = data_json.get("image", None)
            message_db[email + password].append({"role": "user", "content": Query})
            new_query = QueryModifier(Query)
            Decision, dmm_history = \
                await asyncio.to_thread(
                FirstLayerDMM,
                new_query,
                dmm_history
                )
            print(f"{Decision = }")
            g = any([i for i in Decision if i.startswith("general")])
            r = any([i for i in Decision if i.startswith("realtime")])
            mearged_q = " and ".join(
                        [
                            " ".join(
                            i.split()[1:]
                            ) for i in Decision if i.startswith("general") or i.startswith("realtime")
                        ]
                    )
            if Image:
                answer, message_db[email + password] = await asyncio.to_thread(
                    ChatBotAI,
                    mearged_q,
                    Image,
                    message_db[email + password],
                    user_details
                )
                print(f"{answer = }")
                await websocket.send_text(json.dumps({"answer": answer}))
                byt = await TextToSpeechBytes(answer)
                await websocket.send_text(
                        json.dumps({
                        "audio":base64.b64encode(byt).decode('utf-8')
                        })
                    )

            elif g or r:
                if g and r or r:
                    answer, message_db[email + password] = await asyncio.to_thread(
                        RealtimeSearchEngine,
                        mearged_q,
                        message_db[email + password],
                        user_details
                        )
                    await websocket.send(json.dumps({"answer": answer, "display":f'''<span class = "User">{Username}</span> : {answer}'''}))
                    byt = await TextToSpeechBytes(answer)
                    await websocket.send_text(
                        json.dumps({
                        "audio":base64.b64encode(byt).decode('utf-8')
                        })
                    )
                else:
                    answer, message_db[email + password] = await asyncio.to_thread(
                        GeneralChatBot,
                        mearged_q,
                        message_db[email + password],
                        user_details
                        )
                    await websocket.send_text(json.dumps({"answer": answer, "display":f'''<span class = "User">{Username}</span> : {answer}'''}))
                    byt = await TextToSpeechBytes(answer)
                    await websocket.send_text(
                        json.dumps({
                        "audio":base64.b64encode(byt).decode('utf-8')
                        })
                    )

            funcs = ["open","play","generate image","content","google search","youtube search"]
            funcused = [i for i in Decision if any([i.startswith(j) for j in funcs])]
            tosend = []
            for fun in funcused:
                if fun == "open webcam":
                    tosend.append({"cam": "on"})
                    continue
                elif fun == "close webcam":
                    tosend.append({"cam": "off"})
                    continue
                if fun.startswith("open"):
                    tosend.append({
                        "open": wopen(
                            fun.removeprefix("open ")
                            )
                        }
                    )
                elif fun.startswith("play"):
                    url = playonyt(
                        fun.removeprefix("play "),
                        open_video=False
                    )
                    tosend.append({
                        "open": url
                    })
                elif fun.startswith("youtube search"):
                    tosend.append({"open": 'https://www.youtube.com/results?search_query='+fun.removeprefix("youtube search ")})
                elif fun.startswith("generate image"):
                    ...
                elif fun.startswith("content"):
                    tosend.append(
                        {
                            "content":
                            create_content_url(
                                await asyncio.to_thread(
                                    Content,
                                    fun.removeprefix("content "),
                                )
                            )
                        }
                    )
                elif fun.startswith("google search"):
                    tosend.append({"google search ": "https://www.google.com/search?q="+fun.removeprefix("google search ")})
            if tosend:
                await websocket.send_text(json.dumps({"func": tosend}))

    except WebSocketDisconnect:
        print("Client disconnected")

@app.get("/notepad", response_class=HTMLResponse)
async def read_item(request: Request, content: str = "Start typing..."):
    return templates.TemplateResponse("notepad.html", {"request": request, "content": content})

@app.get("/download")
async def download_file(content: str = Query(..., description="Content to be included in the file")):
    # Create an in-memory file-like object
    file_like = io.BytesIO(content.encode('utf-8'))
    file_like.seek(0)
    
    # Create a StreamingResponse
    response = StreamingResponse(
        file_like,
        media_type='application/octet-stream',
        headers={"Content-Disposition": "attachment; filename=text.txt"}
    )
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="192.168.1.6", port=8000)
    # ssh -R 80:192.168.1.6:8000 nokey@localhost.run 