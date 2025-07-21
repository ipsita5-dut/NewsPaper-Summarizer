# from flask import Flask, request, jsonify
# from transformers import pipeline
# import requests
# from bs4 import BeautifulSoup

# # Initialize the Flask application
# app = Flask(__name__)

# # Load the summarization model
# summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# # Function to fetch article text from a URL
# def fetch_article(url):
#     try:
#         response = requests.get(url)
#         response.raise_for_status()  # Raise an error for bad responses
#         soup = BeautifulSoup(response.content, 'html.parser')

#         # Extract text from the article
#         # This may vary depending on the website structure
#         paragraphs = soup.find_all('p')
#         article_text = ' '.join([para.get_text() for para in paragraphs])
#         return article_text
#     except Exception as e:
#         return str(e)

# # Define a route for summarization
# @app.route('/summarize', methods=['POST'])
# def summarize():
#     # Get the JSON data from the request
#     data = request.json
#     url = data.get('url', '')

#     # Fetch the article text from the URL
#     article_text = fetch_article(url)

#     if not article_text:
#         return jsonify({"error": "Could not fetch article from the provided URL."}), 400

#     # Generate the summary
#     summary = summarizer(article_text, max_length=130, min_length=30, do_sample=False)

#     # Return the summary as JSON
#     return jsonify(summary)

# # Run the application
# if __name__ == '__main__':
#     app.run(debug=True)


# from flask import Flask, request, jsonify
# from transformers import BartForConditionalGeneration, BartTokenizer
# import requests
# from flask_cors import CORS  # Import CORS

# from bs4 import BeautifulSoup

# # Initialize the Flask application
# app = Flask(__name__)
# CORS(app)  # Enable CORS for all routes


# model_name = "facebook/bart-large-cnn"

# # Load the tokenizer and model
# tokenizer = BartTokenizer.from_pretrained(model_name)
# model = BartForConditionalGeneration.from_pretrained(model_name)

# # Function to fetch article text from a URL
# def fetch_article(url):
#     try:
#         response = requests.get(url)
#         response.raise_for_status()  # Raise an error for bad responses
#         soup = BeautifulSoup(response.content, 'html.parser')

#         # Extract text from the article
#         paragraphs = soup.find_all('p')
#         article_text = ' '.join([para.get_text() for para in paragraphs])
#         return article_text
#     except Exception as e:
#         return str(e)

# # Define a route for summarization
# @app.route('/summarize', methods=['POST'])
# def summarize():
#     # Get the JSON data from the request
#     data = request.json
#     url = data.get('url', '')

#     # Fetch the article text from the URL
#     article_text = fetch_article(url)

#     if not article_text:
#         return jsonify({"error": "Could not fetch article from the provided URL."}), 400

#     # Tokenize the article text
#     tokens = tokenizer(article_text, truncation=True, padding="longest", return_tensors="pt", max_length=1024)

#     # Generate the summary
#     summary_ids = model.generate( tokens['input_ids'],  # Use the input IDs from the tokenization
#         max_length=300,  # Increase max_length for a more detailed summary
#         min_length=100,  # Set a minimum length
#         length_penalty=1.5,  # Adjust length penalty to favor longer summaries
#         num_beams=6,  # Increase the number of beams for better quality
#         early_stopping=True)
#     summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

#     # Return the summary as JSON
#     return jsonify({"summary": summary})

# # Run the application
# if __name__ == '__main__':
#     app.run(debug=True, port=5001)

from flask import Flask, request, jsonify
from transformers import BartForConditionalGeneration, BartTokenizer
import requests
from flask_cors import CORS
from bs4 import BeautifulSoup
import langid  # Language detection library

# Initialize the Flask application
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load the English summarization model
english_model_name = "facebook/bart-large-cnn"
english_tokenizer = BartTokenizer.from_pretrained(english_model_name)
english_model = BartForConditionalGeneration.from_pretrained(english_model_name)

# Load the Bengali summarization model (you may need to find a suitable model)
bengali_model_name = "facebook/bart-large-mnli"  # Replace with a Bengali model if available
bengali_tokenizer = BartTokenizer.from_pretrained(bengali_model_name)
bengali_model = BartForConditionalGeneration.from_pretrained(bengali_model_name)

# Function to fetch article text from a URL
def fetch_article(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract text from the article
        paragraphs = soup.find_all('p')
        article_text = ' '.join([para.get_text() for para in paragraphs])
        return article_text
    except Exception as e:
        return str(e)

# Define a route for summarization
@app.route('/summarize', methods=['POST'])
def summarize():
    # Get the JSON data from the request
    data = request.json
    url = data.get('url', '')

    # Fetch the article text from the URL
    article_text = fetch_article(url)

    if not article_text:
        return jsonify({"error": "Could not fetch article from the provided URL."}), 400

    # Detect the language of the article
    lang, _ = langid.classify(article_text)

    if lang == 'bn':  # Bengali detected
        tokenizer = bengali_tokenizer
        model = bengali_model
    else:  # Assume English if no Bengali detected
        tokenizer = english_tokenizer
        model = english_model

    # Tokenize the article text
    tokens = tokenizer(article_text, truncation=True, padding="longest", return_tensors="pt", max_length=1024)

    # Generate the summary
    summary_ids = model.generate(
        tokens['input_ids'],
        max_length=300,
        min_length=100,
        length_penalty=1.5,
        num_beams=6,
        early_stopping=True
    )
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    # Return the summary as JSON
    return jsonify({"summary": summary})

# Run the application
if __name__ == '__main__':
    app.run(debug=True, port=5001)