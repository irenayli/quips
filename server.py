from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/translate', methods=['POST'])
def translate():
    data = request.get_json()

    request_error = None
    if 'text' not in data:
        request_error = 'No text provided'
    if 'target_lang' not in data:
        request_error = 'No "target_lang" (target language) provided'
    if 'correlation' not in data:
        request_error = 'No "correlation" (closeness to target language) provided'
    
    if request_error:
        return jsonify({'error': request_error}), 400
    
    return jsonify({'text': data['text']})


if __name__ == '__main__':
    app.run(debug=True)
