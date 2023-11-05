from flask import Flask, request, jsonify
import json
from extract_keyword import extract_keyword

app = Flask(__name__)

@app.route('/echo_call', methods=['POST']) #post echo api
def post_echo_call():
    param = request.get_json()
    return jsonify(param)

@app.route('/keyword') #get echo api
def get_echo_call():
    param = request.args.get('param')
    keyword = extract_keyword(param)
    
    return jsonify({'text': param, "keywords": keyword})

@app.route('/keyword') #get echo api
def get_echo_call():
    param = request.args.get('param')
    keyword = extract_keyword(param)
    
    return jsonify({'text': param, "keywords": keyword})

if __name__ == "__main__":
    app.run(host='0.0.0.0')