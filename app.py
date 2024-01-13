import time
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from flask import Flask, request, jsonify
from fake_review_model import scrape_and_extract, is_ecommerce_url, clear_and_write_file

nltk.download('vader_lexicon')  # Download NLTK data

app = Flask(__name__)

def analyze_sentiments(reviews):
    sia = SentimentIntensityAnalyzer()
    real_count = 0
    fake_count = 0

    for review in reviews:
        sentiment_scores = sia.polarity_scores(review)
        if sentiment_scores['compound'] >= 0.05:
            real_count += 1
        elif sentiment_scores['compound'] <= -0.05:
            fake_count += 1

    total_reviews = real_count + fake_count
    real_percentage = (real_count / total_reviews) * 100
    fake_percentage = (fake_count / total_reviews) * 100

    return real_percentage, fake_percentage

@app.route('/analyze', methods=['POST'])
def analyze_url():
    data = request.json
    url = data.get('url')

    try:
        if is_ecommerce_url(url):
            reviews = scrape_and_extract(url)
            clear_and_write_file('reviews.txt', reviews)

            real_percentage, fake_percentage = analyze_sentiments(reviews)

            analysis_results = {
                'is_ecommerce': True,
                'reviews_count': len(reviews),
                'real_percentage': real_percentage,
                'fake_percentage': fake_percentage,
                'message': 'Reviews scraped,  and written to file'
            }
        else:
            analysis_results = {
                'is_ecommerce': False,
                'message': 'Not an ecommerce URL'
            }
    except Exception as e:
        return jsonify({'error': 'An error occurred'})

    return jsonify(analysis_results)

if __name__ == '__main__':
    app.run(debug=True)
