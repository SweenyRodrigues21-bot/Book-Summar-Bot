# Book-Summar-Bot
#**Summary**

This project is a **Book Summary Bot** that generates concise summaries from text or images of passages.  
Users can either paste text or upload an image, and the system processes the input to provide a clear and easy-to-understand summary.

---

## ✨ Features
- Extract text from uploaded images using **Tesseract OCR** 🖼️
- Process text and generate summaries 📖
- Perform basic sentiment analysis 😊😐😞
- Easy-to-use **Streamlit** web interface 🚀

---

## 🛠️ Installation Guide

### 1. Clone this repository
git clone https://github.com/your-username/Book-Summar-Bot.git
cd Book-Summar-Bot
### 2. Create & activate virtual environment + install requirements
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
### 3. Install Tesseract OCR
C:\Program Files\Tesseract-OCR\tesseract.exe
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe" (set your path)
### 4. Download NLTK resources (first time only)
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('vader_lexicon')
### 5. Run the application
streamlit run app3.py

