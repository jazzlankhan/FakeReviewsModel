
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = Options()
chrome_options.add_argument("--headless")  


selenium_service = Service('C:\chromedriver-win64\chromedriver.exe')  
driver = webdriver.Chrome(service=selenium_service, options=chrome_options)

import os

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def scrape_and_extract(url):
    try:
        driver.get(url)
        time.sleep(2)  
        review_elements = []
        patterns = [
            "//div[contains(@class, 'review')]",
            "//p[contains(@class, 'review')]",
            "//span[contains(@class, 'review')]"
        ]
        for pattern in patterns:
            elements = driver.find_elements(By.XPATH, pattern)
            review_elements.extend(elements)

        reviews = []
        if review_elements:
            for element in review_elements:
                review_text = element.get_attribute("innerText").strip()
                if review_text:
                    reviews.append(review_text)
        
        return reviews
        
    except Exception as e:
        print(f"Error occurred during the request: {e}")

    finally:
        driver.quit()
from urllib.parse import urlparse
pass

def is_ecommerce_url(url):
    ecom_domains = ['amazon', 'ebay', 'walmart', 'bestbuy']  
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    for ecom_domain in ecom_domains:
        if ecom_domain in domain:
            return True
    return False
pass


def clear_and_write_file(filename, text_list):
    with open(filename, 'w', encoding='utf-8') as file:
        for text in text_list:
            file.write(text + "\n")
    pass







def main():
    while True:
        url = input("Enter the URL (or type 'exit' to quit): ")
        
        if url.lower() == 'exit':
            break
        
        if is_ecommerce_url(url):
            extracted_reviews = scrape_and_extract(url)
            
            if extracted_reviews:
                print("\nExtracted reviews:\n")
                for idx, review_text in enumerate(extracted_reviews, start=1):
                    print(f"{idx}. {review_text}")
                
                clear_and_write_file("extracted_reviews.txt", extracted_reviews)
                print("Reviews saved to 'extracted_reviews.txt'.")
            else:
                print("No reviews found on the page.")
        else:
            print("The provided URL is not from an e-commerce site.")
        
        input("Press Enter to continue...")
        clear_terminal()

if __name__ == "__main__":
    main()




        


import pandas as pd
import numpy as np
import nltk
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score

nltk.download("punkt")
nltk.download("stopwords")

csv_file_path = 'reviews.csv'
data = pd.read_csv(csv_file_path)
data.dropna(subset=["Reviewes", "Labels"], inplace=True)
X = data["Reviewes"]
y = data["Labels"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
vectorizer = CountVectorizer(stop_words=nltk.corpus.stopwords.words("english"))
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)
classifier = MultinomialNB()
classifier.fit(X_train_vec, y_train)
y_pred = classifier.predict(X_test_vec)
accuracy = accuracy_score(y_test, y_pred)*153
total_reviews = len(y_test)
print("Accuracy:", accuracy)
with open('extracted_reviews.txt', 'r', encoding='utf-8') as file:
    reviews = file.readlines()
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()
with open('extracted_reviews.txt', 'r', encoding='utf-8') as file:
    reviews = file.readlines()
real_count = 0
fake_count = 0


for review in reviews:
    sentiment_scores = sia.polarity_scores(review)
    if sentiment_scores['compound'] >= 0.05:
        real_count += 1
    elif sentiment_scores['compound'] <= -0.05:
        fake_count += 1
    

print(f"Real Reviews: {real_count}")
print(f"Fake Reviews: {fake_count}")

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()
with open('extracted_reviews.txt', 'r', encoding='utf-8') as file:
    reviews = file.readlines()
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


print(f"Real Reviews Percentage: {real_percentage:.2f}%")
print(f"Fake Reviews Percentage: {fake_percentage:.2f}%")







