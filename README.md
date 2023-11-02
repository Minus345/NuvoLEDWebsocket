# Nuvoled Websocket

Websocket for controlling the nuvoled java software remotely using flaks.

Development:
`flask --app main --debug run`  
`flask --app flaskr run --debug`
Production:
https://flask.palletsprojects.com/en/2.3.x/tutorial/deploy/

`pip install -e .`  
`python -m build --wheel`  
`waitress-serve --call 'flaskr:create_app'`  

start parameter:  
**{  
    "brightness" : "1",  
    "px": 1,  
    "py": 1,  
    "rotation": 90,  
    "screennumber": 0  
}**

