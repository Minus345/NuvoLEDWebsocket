from flask import Flask, request

app = Flask(__name__)

model = []


@app.get('/friend')
def get_friends():
    return model


@app.get('/friend/<int:id>')
def get_one_friend(id):
    return model[id], 200


@app.post('/friend')
def create_friend():
    request_data = request.get_json()
    new_friend = {"name": request_data["name"], "id": len(model)}
    model.append(new_friend)
    return new_friend, 201


@app.delete('/friend/<int:id>')
def delete_friend(id):
    del model[id]
    return {"success": "data successfully deleted from the server"}, 200
