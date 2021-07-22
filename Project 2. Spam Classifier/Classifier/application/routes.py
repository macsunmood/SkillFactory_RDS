# classifier/application/routes.py
from flask import Flask, request, jsonify, send_from_directory
from application import app
from spam_classifier import classify

# Cкрипт run.py находится на верхнем уровне и содержит всего одну строку, которая
# импортирует экземпляр приложения: from application import app

# @app.route('/favicon.ico')
# def favicon():
#     return send_from_directory(app.root_path, #os.path.join(app.root_path, 'static'), 
#     	'favicon.ico', mimetype = 'image/vnd.microsoft.icon')

@app.route('/')
# Декоратор @app.route создает связь между URL-адресом, заданным как 
# аргумент (/), и функцией hello_world().  Это означает, что когда веб-браузер
# запрашивает этот URL-адрес, Flask будет вызывать эту функцию и передавать ее 
# возвращаемое значение обратно в браузер в качестве ответа.
def homepage():
	return '''
    <title>SPAM Classifier</title>
    <center>
        <h1 style="color: #4485b8;">
    		<span style="background-color: #4485b8; color: #ffffff; padding: 0 5px;">SPAM Classifier</span> by Anton Sh. v0.2
    	</h1>
        <form action="/classify_text" method="POST">
            <textarea style="font-size: 14pt" cols="50" rows="10" name="Text" placeholder="email" required="required" /></textarea>
            <br>
            <button style="width:520px; font-size: 14pt" type="submit" class="btn btn-primary btn-block btn-large">Classify</button>
        </form>
    </center>
	'''

@app.route('/classify_text', methods = ['POST'])
def classify_text():
    data = request.form
    # text = data.get('text') # Метод возвращает None, если запрашиваемого ключа нет
    text = data['Text']
    if text is None:
        params = ', '.join(data.keys())
        # Преобразуем все полученные параметры в строку
        return f'Parameter "{params}" is invalid', 400
        # Ранее мы не указывали код ответа HTTP явно,
        # но на самом деле Flask выполнял эту работу за нас. 
        # По умолчанию возвращается 200
    else:
        return '<center>' + homepage() + '<h2 style="color: #880002;">' + classify(text) + '</h2></center>'
    # regex = re.compile('[^a-zA-Z\ ]')
    # data = request.form
    # text = regex.sub('', data['Text'])
    # output = model.classify(text)
    # return render_template('index.html', prediction_text='SPAM: {}'.format(output))

@app.route('/classify_text_api', methods = ['POST'])
def classify_text_api():
    data = request.json
    text = data.get('text') # Метод возвращает None, если запрашиваемого ключа нет
    if text is None:
    	params = ', '.join(data.keys())
    	# Преобразуем все полученные параметры в строку
    	return jsonify({'message': f'Parameter "{params}" is invalid'}), 400
        # Ранее мы не указывали код ответа HTTP явно,
        # но на самом деле Flask выполнял эту работу за нас. 
        # По умолчанию возвращается 200
    else:
    	result = classify(text)
    	return jsonify({'result': result})