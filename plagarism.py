import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Download required NLTK resources
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

def preprocess_text(text):
    # Tokenize the text
    tokens = word_tokenize(text.lower())

    # Remove stop words and punctuation
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token.isalnum() and token not in stop_words]

    # Lemmatize the tokens
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token) for token in tokens] 

    # Join the tokens back into a single string
    processed_text = ' '.join(tokens)
    return processed_text

def calculate_similarity(text1, text2):
    # Preprocess the texts
    processed_text1 = preprocess_text(text1)
    processed_text2 = preprocess_text(text2)

    # Create TF-IDF vectorizer
    vectorizer = TfidfVectorizer()

    # Generate TF-IDF vectors for the processed texts
    tfidf_vectors = vectorizer.fit_transform([processed_text1, processed_text2])

    # Calculate cosine similarity between the vectors
    similarity = cosine_similarity(tfidf_vectors[0], tfidf_vectors[1])[0][0]
    return similarity

def check_plagiarism():
    text1 = text_box1.get("1.0", "end-1c")
    text2 = text_box2.get("1.0", "end-1c")

    if not text1 or not text2:
        messagebox.showwarning("Empty Text", "Please enter both texts.")
        return

    similarity = calculate_similarity(text1, text2)
    if similarity >= 0.8:
        messagebox.showinfo("Plagiarism Detected", "Plagiarism detected!")
    else:
        messagebox.showinfo("No Plagiarism Detected", "No plagiarism detected.")

# Create the main window
window = tk.Tk()
window.title("Plagiarism Checker")

# Set the theme style for the window
style = ttk.Style()
style.theme_use('clam')  # Available themes: 'clam', 'alt', 'default', 'classic'
style.configure('TButton', font=('Arial', 12))
style.configure('TLabel', font=('Arial', 12))

# Create labels and text boxes for input
label1 = ttk.Label(window, text="Text 1:")
label1.pack()
text_box1 = tk.Text(window, height=5, width=50)
text_box1.pack()

label2 = ttk.Label(window, text="Text 2:")
label2.pack()
text_box2 = tk.Text(window, height=5, width=50)
text_box2.pack()

# Create a button to check plagiarism
check_button = ttk.Button(window, text="Check Plagiarism", command=check_plagiarism)
check_button.pack()

# Start the GUI event loop
window.mainloop()
