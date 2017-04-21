import json
from flask import Flask, request, jsonify
from flask_json import FlaskJSON, JsonError
import logging
#import settings
import utils
import textsum
from flask import render_template

app = Flask(__name__)
FlaskJSON(app)

#LOGGER = logging.getLogger("textsum.server")

@app.route("/summary", methods=['POST'])
def getSummarization():
	try:
		result = dict()
		raw = request.get_json(force=True)
		topics = raw['text']
		output = textsum.getSummarizations(topics)
		result['output'] = output
	except Exception as e:
		#LOGGER.info("Summarization Server: " + str(type(e)))
		raise e
	return jsonify(result)

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/summary/one",methods = ['GET', 'POST'])
def login():
	if request.method == "POST":
		try:
			username = request.form.get('username')
			topics = [username]
			output = textsum.getSummarizations(topics)
			result = output[0]
			return "<p>Result: " + result['result'] + "</p><p>Score: " + str(result['score']) + "</p>"
		except:
			return "<h1>Invalid Input.</h1>"    
	else:
		return "<h1>Invalid Input.</h1>"

@app.route("/summary/one", methods=['GET'])
def getSummarizationForOne():
	try:
		raw = request.args
		result = dict()
		topics = [raw[0][1]]
		output = textsum.getSummarizations(topics)
		result['output'] = output
	except Exception as e:
		#LOGGER.info("Summarization Server: " + str(type(e)))
		raise JsonError(description='Invalid Input.')
	return render_template('index.html', name=name)

if __name__ == "__main__":
	#app.run(host='0.0.0.0', port=50110, threaded=True)
	app.run(host='0.0.0.0', port=50110)#, debug=True)
