from flask import request, jsonify, send_from_directory
from application import app
from spam_classifier import NaiveBayesSpamFilter

model = NaiveBayesSpamFilter()
model.train()


@app.route('/')
def homepage():
	return '''
    <title>SPAM Classifier</title>
    <center>
        <h1 style="color: #4485b8;">
    		<span style="background-color: #4485b8; color: #ffffff; padding: 0 5px;">SPAM Classifier</span> v0.2
    	</h1>
        <form action="/classify_text" method="POST">
            <textarea style="font-size: 14pt" cols="50" rows="10" name="Text" placeholder="input text here" required="required" /></textarea>
            <br>
            <button style="width:520px; font-size: 14pt" type="submit" class="btn btn-primary btn-block btn-large">Classify</button>
        </form>
    </center>
	'''

@app.route('/classify_text', methods=['POST'])
def classify_text():
    data = request.form
    text = data['Text']
    if text is None:
        params = ', '.join(data.keys())
        # Convert all the received parameters to a string
        return f'Parameter "{params}" is invalid', 400
    else:
        return '<center>' + homepage() + \
        '<h2><span style="background-color: #880002; color: #ffffff; padding: 0 5px;">' + \
        model.classify(text) + '</span></h2></center>'

@app.route('/classify_text_api', methods=['POST'])
def classify_text_api():
    data = request.json
    text = data.get('text')  # method returns None if the requested key is missing
    if text is None:
    	params = ', '.join(data.keys())
    	# Convert all the received parameters to a string
    	return jsonify({'message': f'Parameter "{params}" is invalid'}), 400
    else:
    	result = model.classify(text)
    	return jsonify({'result': result})