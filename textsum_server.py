import json
from flask import Flask, request, jsonify
from flask_json import FlaskJSON, JsonError
import logging
#import settings
import utils
import textsum

app = Flask(__name__)
FlaskJSON(app)

#LOGGER = logging.getLogger("textsum.server")

@app.route("/summary", methods=['POST'])
def getSummarization():
	try:
		result = dict()
		raw = request.get_json(force=True)
		topics = raw['texts']
		output = textsum.getSummarizations(topics)
		result['output'] = output
	except Exception as e:
		#LOGGER.info("Summarization Server: " + str(type(e)))
		raise e
	return jsonify(result)

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=50110, threaded=True)
