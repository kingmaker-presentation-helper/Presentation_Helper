from flask import Flask, request, jsonify
import json
from extract_keyword import extract_keyword

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "hello_world"

# @app.route('/echo_call/<param>') #get echo api
# def get_echo_call(param):
    
#     file_path = "./test.json"

#     with open(file_path, 'r') as file:
#         data = json.load(file)

#     return jsonify({"points": data})

@app.route('/echo_call', methods=['POST']) #post echo api
def post_echo_call():
    param = request.get_json()
    return jsonify(param)

@app.route('/keyword') #get echo api
def get_echo_call():
    param = request.args.get('param')
    keyword = extract_keyword(param)
    
    # file_path = "./test.json"

    # with open(file_path, 'r') as file:
    #     data = json.load(file)
    return jsonify({'text': param, "keywords": keyword})

if __name__ == "__main__":
    app.run()