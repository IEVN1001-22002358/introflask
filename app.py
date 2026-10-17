from flask import Flask
 
app = Flask(__name__)
 
@app.route('/')
def index():
    return "Hola mundo-- saludo!!!"
 
@app.route("/hola")
def func():
    return " Hola ..."
 
@app.route("/user/<string:user>")
def user(user):
    return " Hola: "+ user
 
@app.route("/numero/<int:n>")
def numero(n):
    return " Numero: {}".format(n)
 
@app.route("/user/<int:id>/<string:username>")
def username(id, username):
    return "ID: {} nombre: {}".format(id, username)
 
@app.route("/suma/<float:n1>/<float:n2>")
def suma(n1, n2):
    return "la suma es: {}".format(n1+n2)
 
if __name__ == "__main__":
    app.run(debug=True)