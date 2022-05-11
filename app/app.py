from flask import Flask, render_template, request, redirect, url_for
import glob
import sys
import re
import string
sys.argv

app=Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def index():

    data = {
        "titulo":"Buscador"
    }

    if request.method == "POST":
        kw = request.form["keywords"]
        return redirect(url_for("result", kw=kw))
    else:
        return render_template("index.html", data=data)


@app.route("/<kw>")
def result(kw):

    #Código de la actividad

    # Si, un ordenamiento burbuja, no, no es broma.
    def bSort(frequency, hits):
        # Doble burbuja
        D1 = {}  # Contiene los valores numericos
        D2 = {}  # Contiene los paths
        result = []

        index = 0
        for i in hits:
            D1[index] = frequency[i]  # Contiene el valor
            D2[index] = i  # Contiene el path
            index += 1

        change = True
        while change:
            change = False
            for i in range(len(hits) - 1):
                if D1[i] < D1[i + 1]:
                    D1[i], D1[i + 1] = D1[i + 1], D1[i]
                    D2[i], D2[i + 1] = D2[i + 1], D2[i]
                    change = True
        index = 0
        for i in range(len(D1)):
            print(D1[i], "   ", D2[i])
            result.append(str(D1[i]) + " " + str(D2[i]))
            index += 1
            if index >= 10:
                break

        return result

    hits = []  # Array donde se escriben los archivos donde se encuentran las palabras.
    keywords = []

    # Seguramente el algoritmo sea en que documentos se repite mas
    frequency = {}

    # keyword = sys.argv[1] if len(sys.argv) >= 2 else input("> Escribe la palabra a buscar: ")
    keywords = [x for x in kw.split()]

    # keyword = keyword.lower()

    filepaths = glob.glob('Files/Files/*')  # Abre el directorio de los archivos donde se buscara la palabra.

    for keyword in keywords:
        keyword = keyword.lower()
        for path in filepaths:
            find = False
            frequency[keyword] = 0
            with open(path, 'r', encoding='ANSI') as file:
                data = file.read().replace('\n', '').lower()

                if data.find(keyword) != -1:
                    words = re.findall(r'\b[a-z]{3,15}\b', data)

                    # Contando la repeticion de palabras para resaltar los relevantes
                    for word in words:
                        if word == keyword:
                            count = frequency.get(keyword, 0)
                            frequency[keyword] = count + 1

                    if not find:
                        find = True

                    equal = False

                    for hit in hits:
                        if hit == path:
                            equal = True

                    frequency[path] = count + 1
                    if not equal:
                        hits.append(path)  # Si encuentra palabra, agregara el archivo al array.

    if not hits:
        print('La palabra buscada no se encontro en ningun archivo.')
        quit()

    print("Top 10 Documents")
    result = bSort(frequency, hits)

    #Lo que voy a regresar:
    data ={
        "kw":result,
        "titulo": "Resultado"
    }
    return render_template("result.html", data=data)


def pagina_no_encontrada(error):
    #return render_template("404.html"), 404
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.register_error_handler(404, pagina_no_encontrada)
    app.run(debug=True,port=8000)