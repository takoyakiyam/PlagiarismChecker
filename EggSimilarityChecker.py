import nltk
import os
import time
from nltk.corpus import stopwords
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from fpdf import FPDF
import PyPDF2
import docx
import markdown
import striprtf
from bs4 import BeautifulSoup
import csv
import json
import xml.etree.ElementTree as ET
import yaml
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Download NLTK resources if not already downloaded
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')

# Define the Jaccard Similarity function
def jaccard_similarity(text1, text2):
    shingles1 = set(text1)
    shingles2 = set(text2)
    intersection = shingles1.intersection(shingles2)
    union = shingles1.union(shingles2)
    return len(intersection) / len(union) if len(union) > 0 else 0

# Define the function to extract text from various file types
def open_file(text_entry):
    filename = filedialog.askopenfilename(
        title="Select a File",
        filetypes=[
            ("Text files", "*.txt"),
            ("Microsoft Word", "*.docx"),
            ("PDF files", "*.pdf"),
            ("Markdown files", "*.md"),
            ("Rich Text Format", "*.rtf"),
            ("HTML files", "*.html;*.htm"),
            ("Comma-Separated Values", "*.csv"),
            ("JSON files", "*.json"),
            ("XML files", "*.xml"),
            ("LaTeX files", "*.tex"),
            ("YAML files", "*.yaml;*.yml"),
        ],
    )
    if filename:
        try:
            if filename.endswith(".txt"):
                with open(filename, 'r') as f:
                    text_entry.delete("1.0", tk.END)
                    text_entry.insert("1.0", f.read())
            elif filename.endswith(".docx"):
                doc = docx.Document(filename)
                extracted_text = '\n'.join(para.text for para in doc.paragraphs)
                text_entry.delete("1.0", tk.END)
                text_entry.insert("1.0", extracted_text)
            elif filename.endswith(".pdf"):
                with open(filename, 'rb') as pdf_file:
                    pdf_reader = PyPDF2.PdfReader(pdf_file)
                    extracted_text = "".join(
                        page.extract_text() for page in pdf_reader.pages
                    )
                text_entry.delete("1.0", tk.END)
                text_entry.insert("1.0", extracted_text)
            elif filename.endswith(".md"):
                with open(filename, 'r') as f:
                    markdown_text = markdown.markdown(f.read())
                    text_entry.delete("1.0", tk.END)
                    text_entry.insert("1.0", markdown_text)
            elif filename.endswith(".rtf"):
                with open(filename, 'r') as f:
                    rtf_text = striprtf.striprtf(f.read())
                    text_entry.delete("1.0", tk.END)
                    text_entry.insert("1.0", rtf_text)
            elif filename.endswith((".html", ".htm")):
                with open(filename, 'r') as f:
                    soup = BeautifulSoup(f.read(), "html.parser")
                    html_text = soup.get_text()
                    text_entry.delete("1.0", tk.END)
                    text_entry.insert("1.0", html_text)
            elif filename.endswith(".csv"):
                csv_text = []
                with open(filename, newline='') as f:
                    reader = csv.reader(f)
                    for row in reader:
                        csv_text.append(", ".join(row))
                    csv_text = "\n".join(csv_text)
                text_entry.delete("1.0", tk.END)
                text_entry.insert("1.0", csv_text)
            elif filename.endswith(".json"):
                with open(filename, 'r') as f:
                    json_data = json.load(f)
                    json_text = json.dumps(json_data, indent=4)
                    text_entry.delete("1.0", tk.END)
                    text_entry.insert("1.0", json_text)
            elif filename.endswith(".xml"):
                with open(filename, 'r') as f:
                    tree = ET.parse(f)
                    root = tree.getroot()
                    xml_text = ET.tostring(root, encoding='utf-8', method='text').decode("utf-8")
                    text_entry.delete("1.0", tk.END)
                    text_entry.insert("1.0", xml_text)
            elif filename.endswith((".yaml", ".yml")):
                with open(filename, 'r') as f:
                    yaml_data = yaml.safe_load(f)
                    yaml_text = yaml.dump(yaml_data, indent=4)
                    text_entry.delete("1.0", tk.END)
                    text_entry.insert("1.0", yaml_text)
            else:
                print(f"Unsupported file type: {filename}")
        except Exception as e:
            print(f"Error opening file: {e}")

# Define the scheduling algorithms with actual processing logic
def round_robin(text1, text2, chunk_size=25):
    start_time = time.time()
    # Simulate processing logic by iterating through text in chunks
    chunks1 = [text1[i:i+chunk_size] for i in range(0, len(text1), chunk_size)]
    chunks2 = [text2[i:i+chunk_size] for i in range(0, len(text2), chunk_size)]
    similar_count = 0
    for chunk1, chunk2 in zip(chunks1, chunks2):
        if chunk1 == chunk2:
            similar_count += 1
        time.sleep(0.01)  # Simulate processing time for each chunk
    end_time = time.time()
    finish_time = end_time - start_time
    return "Round Robin", finish_time, similar_count

def shortest_job_next(text1, text2):
    start_time = time.time()
    # Simulate processing logic by processing the shorter text first
    short_text, long_text = (text1, text2) if len(text1) <= len(text2) else (text2, text1)
    similar_count = 0
    for i in range(len(short_text)):
        if short_text[i] == long_text[i]:
            similar_count += 1
        time.sleep(0.01)  # Simulate processing time for each character
    for i in range(len(short_text), len(long_text)):
        time.sleep(0.01)  # Continue processing the longer text
    end_time = time.time()
    finish_time = end_time - start_time
    return "Shortest Job Next", finish_time, similar_count

def priority_scheduling(text1, text2):
    start_time = time.time()
    # Simulate processing logic by prioritizing word-level similarity
    words1 = text1.split()
    words2 = text2.split()
    similar_count = 0
    for word1, word2 in zip(words1, words2):
        if word1 == word2:
            similar_count += 1
        time.sleep(0.01)  # Simulate processing time for each word
    end_time = time.time()
    finish_time = end_time - start_time
    return "Priority Scheduling", finish_time, similar_count

# Determine which scheduling algorithm to use based on selection
def get_scheduling_algorithm(algo, text1, text2, chunk_size=25):
    if algo == "Round Robin":
        return round_robin(text1, text2, chunk_size)
    elif algo == "Shortest Job Next":
        return shortest_job_next(text1, text2)
    elif algo == "Priority Scheduling":
        return priority_scheduling(text1, text2)
    else:
        return "No algorithm selected.", 0, 0

def check_similarity(text_entry1, text_entry2, result_label, algo, chunk_size=None):
    if algo == "Round Robin" and chunk_size is None:
        chunk_size = 25

    text1 = text_entry1.get("1.0", tk.END)[:-1].lower()
    text2 = text_entry2.get("1.0", tk.END)[:-1].lower()

    # Remove stop words (optional)
    stop_words = stopwords.words('english')
    text1_filtered = [word for word in text1.split() if word not in stop_words]
    text2_filtered = [word for word in text2.split() if word not in stop_words]

    # Perform TF-IDF vectorization on the entire texts
    vectorizer = TfidfVectorizer()
    combined_texts = [' '.join(text1_filtered), ' '.join(text2_filtered)]
    tfidf_matrix = vectorizer.fit_transform(combined_texts)

    # Cosine similarity with TF-IDF vectors
    similarity_tfidf = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])

    # Parts of Speech Tagging
    text1_pos = nltk.pos_tag(nltk.word_tokenize(text1))
    text2_pos = nltk.pos_tag(nltk.word_tokenize(text2))

    # Perform lemmatization or stemming
    wnl = nltk.WordNetLemmatizer()
    text1_lemma = [wnl.lemmatize(word) for word, pos in text1_pos]
    text2_lemma = [wnl.lemmatize(word) for word, pos in text2_pos]

    # Jaccard similarity with word-level check
    similarity_word = jaccard_similarity(tuple(text1_filtered), tuple(text2_filtered))

    # Jaccard similarity with lemmatized words
    similarity_lemma = jaccard_similarity(tuple(text1_lemma), tuple(text2_lemma))

    # Count of similar words
    similar_word_count = len(set(text1_filtered).intersection(set(text2_filtered)))

    # Apply selected algorithm for text processing
    algo_name, processing_time, similar_count = get_scheduling_algorithm(algo, text1, text2, chunk_size)

    # Calculate similarity percentage
    similarity_percentage = (similar_word_count / len(set(text1_filtered).union(set(text2_filtered)))) * 100

    result_text = f"Similarity Score (Word Level):       {similarity_word:.2f}\n"
    result_text += f"Similarity Score (Lemmatized):      {similarity_lemma:.2f}\n"
    result_text += f"Cosine Similarity Score (TF-IDF):   {similarity_tfidf[0][0]:.2f}\n"
    result_text += f"Count of Similar Words:             {similar_word_count}\n"
    result_text += f"Similarity Percentage:              {similarity_percentage:.2f}%\n"
    result_text += f"Scheduling Algorithm:               {algo_name}\n"
    result_text += f"Processing Time:                    {processing_time:.2f} seconds\n"
    result_text += f"Similar Count from Algorithm:       {similar_count}\n"

    result_text += "\n\n------------------ Similarity Detection Result ------------------\n\n"
    if similarity_percentage >= 80:  # High Threshold for Similarity
        result_text += "Metric:                   Similarity Detection\n"
        result_text += "Similarity Percentage:    {:.2f}%\n".format(similarity_percentage)
        result_text += "Result:                   High similarity detected!\n"
        result_text += "Description:              Identical or very similar content detected.\n"
        result_label.config(foreground="red", text=result_text)
    elif similarity_percentage >= 50:  # Medium Threshold for Similarity
        result_text += "Metric:                   Similarity Detection\n"
        result_text += "Similarity Percentage:    {:.2f}%\n".format(similarity_percentage)
        result_text += "Result:                   Moderate similarity detected!\n"
        result_text += "Description:              Possible paraphrasing or close rephrasing of the source material.\n"
        result_label.config(foreground="orange", text=result_text)
    else:
        result_text += "Metric:                   Similarity Detection\n"
        result_text += "Similarity Percentage:    {:.2f}%\n".format(similarity_percentage)
        result_text += "Result:                   Low similarity detected.\n"
        result_text += "Description:              No strong evidence of similarity.\n"
        result_label.config(foreground="green", text=result_text)

    def save_as_pdf():
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # Create a table for the statistical results
        pdf.cell(0, 10, "Statistical Results", 1, 1, "C")

        pdf.cell(95, 10, "Metric", 1, 0, "C")
        pdf.cell(95, 10, "Value", 1, 0, "C")
        pdf.ln(10)

        pdf.cell(95, 10, "Jaccard Similarity Score (Word Level)", 1, 0, "C")
        pdf.cell(95, 10, f"{similarity_word:.2f}", 1, 0, "C")
        pdf.ln(10)

        pdf.cell(95, 10, "Jaccard Similarity Score (Lemmatized)", 1, 0, "C")
        pdf.cell(95, 10, f"{similarity_lemma:.2f}", 1, 0, "C")
        pdf.ln(10)

        pdf.cell(95, 10, "Cosine Similarity Score (TF-IDF)", 1, 0, "C")
        pdf.cell(95, 10, f"{similarity_tfidf[0][0]:.2f}", 1, 0, "C")
        pdf.ln(10)

        pdf.cell(95, 10, "Count of Similar Words", 1, 0, "C")
        pdf.cell(95, 10, f"{similar_word_count}", 1, 0, "C")
        pdf.ln(10)

        pdf.cell(95, 10, "Similarity Percentage", 1, 0, "C")
        pdf.cell(95, 10, f"{similarity_percentage:.2f}%", 1, 0, "C")
        pdf.ln(10)

        pdf.cell(95, 10, "Scheduling Algorithm", 1, 0, "C")
        pdf.cell(95, 10, f"{algo_name}", 1, 0, "C")
        pdf.ln(10)

        pdf.cell(95, 10, "Processing Time", 1, 0, "C")
        pdf.cell(95, 10, f"{processing_time:.2f} seconds", 1, 0, "C")
        pdf.ln(10)

        pdf.cell(95, 10, "Similar Count from Algorithm", 1, 0, "C")
        pdf.cell(95, 10, f"{similar_count}", 1, 0, "C")
        pdf.ln(20)

        pdf.ln(10)
        if similarity_percentage >= 80:  # High Threshold for Similarity
            pdf.cell(0, 10, "--------- Similarity Detection Result ---------", 0, 1, "C")
            pdf.ln(10)
            pdf.cell(0, 10, f"High similarity detected, possible copying found! ({similarity_percentage:.2f})%", 0, 1, "C")
            pdf.ln(10)
            pdf.cell(0, 10, "Description: Identical or very similar content detected.", 0, 1, "C")
        elif similarity_percentage >= 50:  # Medium Threshold for Potential Similarity
            pdf.cell(0, 10, "--------- Similarity Detection Result ---------", 0, 1, "C")
            pdf.ln(10)
            pdf.cell(0, 10, f"Moderate similarity detected, potential copying found! ({similarity_percentage:.2f})%", 0, 1, "C")
            pdf.ln(10)
            pdf.cell(0, 10, "Description: Possible paraphrasing or close rephrasing of the source material.", 0, 1, "C")
        else:
            pdf.cell(0, 10, "--------- Similarity Detection Result ---------", 0, 1, "C")
            pdf.ln(10)
            pdf.cell(0, 10, f"Low similarity detected, no strong evidence of copying. ({similarity_percentage:.2f})%", 0, 1, "C")
            pdf.ln(10)
            pdf.cell(0, 10, "Description: No similarity detected.", 0, 1, "C")

        # Determine a unique filename
        base_filename = "similarity_report"
        extension = ".pdf"
        counter = 1
        filename = base_filename + extension
        while os.path.exists(filename):
            counter += 1
            filename = f"{base_filename}_{counter}{extension}"

        pdf.output(filename)
        messagebox.showinfo("PDF Saved", f"Similarity report saved as {filename}")

    save_pdf_button = ttk.Button(root, text="Save as PDF", command=save_as_pdf)
    save_pdf_button.grid(row=7, column=0, columnspan=2, padx=10, pady=10)
# Show/hide chunk size entry based on selected algorithm
def on_algorithm_change(event, chunk_size_label, chunk_size_entry, algo_var):
    if algo_var.get() == "Round Robin":
        chunk_size_label.grid(row=4, column=0, padx=10, pady=5, sticky=tk.E)
        chunk_size_entry.grid(row=4, column=1, padx=10, pady=5, sticky=tk.W)
    else:
        chunk_size_label.grid_remove()
        chunk_size_entry.grid_remove()

# GUI setup
def main():
    global root
    root = tk.Tk()
    root.title("Document Similarity Checker")

    # Set window size and disable maximizing and full-screen options
    root.geometry("850x850")  # Set the desired window size

    # Make the rows and columns resizable
    for i in range(6):
        root.grid_rowconfigure(i, weight=1)
    for i in range(2):
        root.grid_columnconfigure(i, weight=1)

    # Text Entry Boxes
    style = ttk.Style()
    style.configure("TText", borderwidth=1, relief="solid", font=("Helvetica", 10))
    style.configure("TLabel", font=("Helvetica", 12))
    style.configure("TButton", font=("Helvetica", 10))
    style.configure("TCombobox", font=("Helvetica", 10))

    text_entry1 = tk.Text(root, height=20, width=50, highlightthickness=1, highlightbackground="black", font=("Helvetica", 10))
    text_entry1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    open_file_button1 = ttk.Button(root, text="Open File 1", command=lambda: open_file(text_entry1))
    open_file_button1.grid(row=1, column=0, padx=10, pady=5, sticky="w")

    word_count_label1 = ttk.Label(root, text="Word Count: 0")
    word_count_label1.grid(row=1, column=0, padx=10, pady=5, sticky="e")

    text_entry2 = tk.Text(root, height=20, width=50, highlightthickness=1, highlightbackground="black", font=("Helvetica", 10))
    text_entry2.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

    open_file_button2 = ttk.Button(root, text="Open File 2", command=lambda: open_file(text_entry2))
    open_file_button2.grid(row=1, column=1, padx=10, pady=5, sticky="w")

    word_count_label2 = ttk.Label(root, text="Word Count: 0")
    word_count_label2.grid(row=1, column=1, padx=10, pady=5, sticky="e")

    def update_word_count_labels():
        text1 = text_entry1.get("1.0", tk.END)[:-1]
        text2 = text_entry2.get("1.0", tk.END)[:-1]
        word_count1 = len(text1.split())
        word_count2 = len(text2.split())
        word_count_label1.config(text=f"Word Count: {word_count1}")
        word_count_label2.config(text=f"Word Count: {word_count2}")
        root.after(100, update_word_count_labels)

    update_word_count_labels()

    # Result Label
    result_label = ttk.Label(root, text="", justify=tk.CENTER, wraplength=700, anchor="center")
    result_label.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

    # Algorithm Selection Dropdown
    algo_label = ttk.Label(root, text="Select Scheduling Algorithm:")
    algo_label.grid(row=3, column=0, padx=10, pady=5, sticky="e")

    algorithms = ["Round Robin", "Shortest Job Next", "Priority Scheduling"]
    algo_var = tk.StringVar(root)
    algo_var.set(algorithms[2])  # Default selection

    algo_dropdown = ttk.Combobox(root, textvariable=algo_var, values=algorithms, state="readonly")
    algo_dropdown.grid(row=3, column=1, padx=10, pady=5, sticky="w")

    # Chunk Size for Round Robin
    chunk_size_label = ttk.Label(root, text="Chunk Size:")
    chunk_size_entry = ttk.Entry(root)
    chunk_size_entry.insert(0, "25")

    # Show/hide chunk size entry based on selected algorithm
    algo_dropdown.bind("<<ComboboxSelected>>", lambda event: on_algorithm_change(event, chunk_size_label, chunk_size_entry, algo_var))

    # Button to check similarity
    check_button = ttk.Button(root, text="Check Similarity", 
                            command=lambda: check_similarity(
                                text_entry1, 
                                text_entry2, 
                                result_label, 
                                algo_var.get(), 
                                int(chunk_size_entry.get()) if algo_var.get() == "Round Robin" else None))
    check_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
