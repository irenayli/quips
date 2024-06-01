from flask import Flask, request, jsonify, render_template
import csv

app = Flask(__name__)

# Load language similarities
iso_to_lang = {}
similarities = None
similarities_path = 'data/language_similarities.tsv'
with open(similarities_path, 'r') as f:
    reader = csv.reader(f, delimiter='\t')
    similarities = list(reader)
    for row in similarities:
        iso_to_lang[row[0]] = row[1]
    
# print(iso_to_lang)
# print(similarities)

# Find one similar language where the correlation is closest to the target correlation
# Returns the full row of the closest language
def get_similar_language(src_lang_iso, target_similarity_normalized):
    # similar_languages = []
    similarity_min = None
    similarity_max = None
    for row in similarities:
        if row[0] == src_lang_iso:
            if similarity_min is None or similarity_min > float(row[4]):
                similarity_min = float(row[4])
            if similarity_max is None or similarity_max < float(row[4]):
                similarity_max = float(row[4])

    print("Similarity range:", similarity_min, similarity_max)
    
    closest = None
    closest_diff = None
    for row in similarities:
        if row[0] == src_lang_iso:
            normalized_similarity = (float(row[4]) - similarity_min) / (similarity_max - similarity_min)
            diff = abs(normalized_similarity - target_similarity_normalized)
            if closest is None or diff < closest_diff:
                closest = row
                closest_diff = diff
    return closest

def get_language_name(iso):
    return iso_to_lang[iso]

print(get_language_name('eng'))
print(get_language_name('spa'))

print(get_similar_language('eng', 0.5))

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
