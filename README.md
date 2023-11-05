# Nuvoled Websocket

Websocket for controlling the nuvoled java software remotely using flaks.

## Development

### Virtual ENV

```bash
pip3 install virtualenv
cd <projekt>
virtualenv venv
source venv/bin/activate
pip3 install build waitress flask psutil queuelib
```

### Start

`flask --app flaskr run --debug`
Production:
https://flask.palletsprojects.com/en/2.3.x/tutorial/deploy/

(`pip install -e .`)  
`python -m build --wheel`  
`cd .\dist\ `  
`pip install .\flaskr-1.0.0-py2.py3-none-any.whl`  
`waitress-serve --call 'flaskr:create_app'`  

start parameter:  
**{  
    "brightness" : "1",  
    "px": 1,  
    "py": 1,  
    "rotation": 90,  
    "screennumber": 0  
}**

