# Text Summarization API

Welcome to the Text Summarization API repository! 📝🚀

## Overview

This API provides a powerful tool for text summarization, built using Python and Flask. It simplifies the process of distilling large amounts of text into concise summaries, making it ideal for various applications such as news aggregation, research synthesis, and content curation.

## Features

- Extractive text summarization using the TextRank algorithm
- Built-in preprocessing for tokenization, stop word removal, and lowercasing
- Customizable summary length
- Easy integration with existing applications
- Accessible via GitHub repository for seamless deployment and usage

## How to Use

1. Clone this repository to your local machine.
2. Run the Flask server by executing `python app.py`.
3. Make POST requests to the `/summarize` endpoint with JSON data containing the text to be summarized.
4. Receive the summarized text as a response!

## Example

```python
import requests

url = 'http://localhost:5000/summarize'
data = {
    'text': 'Your text goes here...',
    'num_sentences': 3
}
response = requests.post(url, json=data)
print(response.json())
