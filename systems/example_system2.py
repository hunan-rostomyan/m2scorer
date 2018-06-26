from flask import Flask
from flask import jsonify
from flask import request

app = Flask(__name__)

preset = {
	"The cat sat at mat .": "A cat sat on mat .",
	"The dog .": "The dog .",
	"Giant otters is an apex predator .": "Giant otters are apex predator ."
}

@app.route('/correct', methods=['POST'])
def correct():
	data = request.get_json()
	return jsonify({'correction': preset[data['sentence']]})
