from flask import Flask, render_template, request
import nltk
from nltk.corpus import wordnet
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import random

app = Flask(__name__, template_folder='template')

# Download NLTK resources
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Initialize stopwords and lemmatizer
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def get_synonyms(word):
    synonyms = []
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonym = lemma.name()
            if synonym.lower() != word.lower():
                synonyms.append(synonym)
    return synonyms

def paraphrase_sentence(sentence):
    words = word_tokenize(sentence)
    paraphrased_sentence = []
    for word in words:
        if word.lower() not in stop_words:
            synonyms = get_synonyms(word)
            if synonyms:
                paraphrased_sentence.append(random.choice(synonyms))
            else:
                paraphrased_sentence.append(word)
        else:
            paraphrased_sentence.append(word)
    return ' '.join(paraphrased_sentence)

def paraphrase_text(text):
    sentences = sent_tokenize(text)
    paraphrased_text = []
    for sentence in sentences:
        paraphrased_text.append(paraphrase_sentence(sentence))
    return ' '.join(paraphrased_text)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/paraphrase', methods=['POST'])
def paraphrase():
    if request.method == 'POST':
        original_text = request.form['text']
        paraphrased_text = paraphrase_text(original_text)
        return render_template('paraphrased.html', original_text=original_text, paraphrased_text=paraphrased_text)

if __name__ == "__main__":
    app.run(debug=True)
