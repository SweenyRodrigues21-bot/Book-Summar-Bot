# 📌 Import Libraries
import nltk
import matplotlib.pyplot as plt
from collections import Counter
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import spacy
import streamlit as st
from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# 📌 Download NLTK Resources
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('vader_lexicon')

# 📌 Load SpaCy Model
try:
    nlp = spacy.load("en_core_web_sm")
except:
    nlp = spacy.blank("en")

#========== FUNCTIONS ==========#

# Summarization
def summarize_text(text, summary_type="medium"):
    sentences = sent_tokenize(text)
    if not sentences:
        return "No text available for summary."
    if summary_type == "short":
        return " ".join(sentences[:2])
    elif summary_type == "medium":
        return " ".join(sentences[:4])
    elif summary_type == "bullet":
        return "\n- " + "\n- ".join(sentences[:5])

# Sentiment Analysis
def analyze_sentiment(text):
    sia = SentimentIntensityAnalyzer()
    score = sia.polarity_scores(text)
    if score['compound'] >= 0.05:
        sentiment = "Positive"
    elif score['compound'] <= -0.05:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"
    return sentiment, score['compound']

# Keyword Extraction
def extract_keywords(text, top_n=10):
    words = word_tokenize(text.lower())
    stop_words = set(stopwords.words('english'))
    filtered_words = [w for w in words if w.isalnum() and w not in stop_words]
    freq = Counter(filtered_words)
    return freq.most_common(top_n)

# Named Entity Recognition
def extract_entities(text):
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities

# Keyword Frequency Chart
def plot_keyword_chart(keywords):
    if not keywords:
        return
    words, counts = zip(*keywords)
    plt.figure(figsize=(8,5))
    plt.bar(words, counts, color="skyblue")
    plt.title("Top Keywords Frequency")
    plt.xlabel("Keywords")
    plt.ylabel("Frequency")
    plt.xticks(rotation=45)
    st.pyplot(plt)

# Golden Lines Extraction
def extract_golden_lines(text, top_n=3):
    sentences = sent_tokenize(text)
    if not sentences:
        return []
    words = word_tokenize(text.lower())
    stop_words = set(stopwords.words('english'))
    keywords = [w for w in words if w.isalnum() and w not in stop_words]

    scored_sentences = []
    for sent in sentences:
        score = sum([1 for w in word_tokenize(sent.lower()) if w in keywords])
        scored_sentences.append((sent, score))

    scored_sentences.sort(key=lambda x: x[1], reverse=True)
    return [sent for sent, score in scored_sentences[:top_n]]

# OCR Function for Images
def extract_text_from_image(image_file):
    img = Image.open(image_file)
    text = pytesseract.image_to_string(img)
    return text

#========== STREAMLIT FRONTEND ==========#
st.title("📚 Book Summary BOT")

# Option Selection
option = st.radio("Choose Input Method:", ["✍️ Paste Text", "🖼️ Upload Image"])

text = ""

if option == "✍️ Paste Text":
    text = st.text_area("Enter your text:", height=200)

elif option == "🖼️ Upload Image":
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
        text = extract_text_from_image(uploaded_file)
        st.success("✅ Text extracted from image!")

# Run Analysis if text available
if text:
    # Summarization
    st.subheader("📖 Summary")
    summary_type = st.selectbox("Choose summary type:", ["short", "medium", "bullet"])
    st.write(summarize_text(text, summary_type))

    # Sentiment Analysis
    st.subheader("😊 Sentiment Analysis")
    sentiment, score = analyze_sentiment(text)
    st.write(f"**Sentiment:** {sentiment} (Score: {score})")

    # Keywords
    st.subheader("🔑 Keywords")
    keywords = extract_keywords(text, 6)
    st.write(keywords)
    if keywords:
        plot_keyword_chart(keywords)

    # Named Entities
    st.subheader("👤 Named Entities")
    entities = extract_entities(text)
    if entities:
        for ent, label in entities:
            st.write(f"{ent} → {label}")
    else:
        st.write("No entities found")

    # Golden Lines
    st.subheader("✨ Golden Lines")
    golden_lines = extract_golden_lines(text)
    if golden_lines:
        for line in golden_lines:
            st.write(f"💡 {line}")
    else:
        st.write("No golden lines found")
