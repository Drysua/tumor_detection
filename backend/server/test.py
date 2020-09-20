from flask import Flask, request, Response
import jsonpickle
import io
import base64
app = Flask(__name__)
 
 
@app.route('/form', methods=['POST', 'GET'])
def form():
    if request.method == 'GET':
        return '''<!doctype html>
                        <html>
                          <head>
                             <title>Пример формы</title>
                          </head>
                          <body>
                            <h1>Форма для регистрации</h1>
                            <div>
                                <form method="post">
                                    <input type="email" placeholder="Введите адрес почты" name="email"><br/>
                                    <input type="password" placeholder="Введите пароль" name="password"><br/>
                                    <button type="submit" >Записаться</button>
                                </form>
                            </div>
                          </body>
                        </html>'''
    elif request.method == 'POST':
        print(request.form['email'])
        print(request.form['password'])
        return "Форма отправлена"

@app.route("/predict", methods = ["POST"])
def upload_file():
     if(request.method == 'POST'):
        img = request.files['file'].read()

        image_string = base64.b64encode(img)
        image_string = image_string.decode('utf-8')

        response = {
            "Labels": image_string
        }

        response_pickled = jsonpickle.encode(response)

        return Response(response=response_pickled, status=200, mimetype="application/json")
