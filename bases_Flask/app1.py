from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
    titulo = "PWA"
    lista = ["Pedro", "Luis", "Paco"]  
    return render_template("index.html", titulo=titulo, lista=lista)

@app.route("/hola")
def func():
    return " Hola ..."

@app.route("/distancia")
def distancia():
    return render_template("Distancia.html")

@app.route("/OperasBas", methods=["GET", "POST"])
def operasBas():
    n1 = ""
    n2 = ""
    res = None
    if request.method == 'POST':
        n1 = request.form.get('n1', '')
        n2 = request.form.get('n2', '')
        operacion = request.form.get('operacion')

        try:
            val1 = float(n1)
            val2 = float(n2)

            if operacion == 'sumar':
                res = val1 + val2
            elif operacion == 'restar':
                res = val1 - val2
            elif operacion == 'multiplicar':
                res = val1 * val2
            elif operacion == 'dividir':
                res = val1 / val2 if val2 != 0 else "Error: División entre cero"
        except (ValueError, TypeError):
            res = "Error en los valores ingresados"

    return render_template("OperasBas.html", n1=n1, n2=n2, res=res)

@app.route("/user/<string:user>")
def user(user):
    return " Hola: " + user

@app.route("/numero/<int:n>")
def numero(n):
    return " Numero: {}".format(n)

@app.route("/user/<int:id>/<string:username>")
def username(id, username):
    return "ID: {} nombre: {}".format(id, username)

@app.route("/suma/<float:n1>/<float:n2>")
def suma(n1, n2):
    return "la suma es: {}".format(n1 + n2)

if __name__ == "__main__":
    app.run(debug=True)