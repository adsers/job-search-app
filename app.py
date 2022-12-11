import os
import sqlite3
from werkzeug.utils import secure_filename
from flask import Flask, flash, redirect, render_template, request, session
import pdfplumber
import string
import spacy
nlp = spacy.load("en_core_web_lg")

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = ['pdf']

# Configure application
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000
app.secret_key = "super secret key"

# Configure sql database
con = sqlite3.connect("master.db", check_same_thread=False)
cur = con.cursor()

def get_words_list(data):
    words_list = list()
    prev_char_fontname = None
    start_index = 0
    end_index = 0
    for index, char_data in enumerate(data):
        char_actual = char_data['text']
        char_fontname = char_data['fontname']
        if char_actual == ' ' or char_fontname != prev_char_fontname:
            # delimiter = True
            end_index = index
        prev_char_fontname = char_fontname
        to_go_list = list()
        for index, char_data in enumerate(data[start_index: end_index]):
            to_go_list.append(char_data['text'])
        start_index = end_index
        if ''.join(to_go_list).strip() != '':
            words_list.append(''.join(to_go_list).strip())
    return words_list

acceptable_chars = string.ascii_letters + string.digits + string.punctuation

def remove_weird_chars(input_str):
    acceptable_chars = string.ascii_letters + string.digits + string.punctuation + ' '
    final_char_list = list()
    for char in input_str:
        if char in acceptable_chars:
            final_char_list.append(char)
    return ''.join(final_char_list)

def get_resume_words(datapath):
    with pdfplumber.open(datapath) as pdf:
        first_page = pdf.pages[0]
        data = first_page.chars
        return remove_weird_chars(' '.join(get_words_list(data)))

def process_text(text):
    doc = nlp(text.lower())
    result = []
    for token in doc:
        if token.text in nlp.Defaults.stop_words:
            continue
        if token.is_punct:
            continue
        if token.lemma_ == '-PRON-':
            continue
        result.append(token.lemma_)
    return " ".join(result)

def calculate_similarity(text1, text2):
    base = nlp(process_text(text1))
    compare = nlp(process_text(text2))
    return base.similarity(compare)

def pretty_percentages(percentage):
    return str(round(percentage*100, 2)) + '%'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET", "POST"])
def index():
    """Shows the homepage"""
    if request.method == "GET":
        return render_template('index.html')
    
    elif request.method == "POST":
        if 'file' not in request.files:
            flash('No file part')
            return render_template("index.html")

        file = request.files['file']
        if file.filename == '':
            flash("No file selected")
            return redirect(request.url)
        if not allowed_file(file.filename):
            flash("Please upload a PDF format file")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            print(type(file))
            print(file.filename)
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('File uploaded successfully!')
            resume_words = get_resume_words(f'./uploads/{filename}')
            desc_list = cur.execute('SELECT description FROM jobs;').fetchall()
            desc_list = [i[0] for i in desc_list]

            match_scores_dict = dict()

            for i, desc in enumerate(desc_list):
                similarity_score = calculate_similarity(resume_words, desc)
                match_scores_dict[i] = similarity_score

            result_idx = sorted(match_scores_dict, key = lambda x: -match_scores_dict[x])[:10]
            return_list = list()
            for idx in result_idx:
                return_list.append(cur.execute(f'SELECT * FROM jobs WHERE unique_index={idx}').fetchall())

            companies_list = [i[0][1] for i in return_list]
            posn_list = [i[0][2] for i in return_list]
            salary_list = [i[0][3] for i in return_list]
            experience_list = [i[0][4] for i in return_list]
            location_list = [i[0][5] for i in return_list]
            jd_list = [i[0][6] for i in return_list]
            link_list = [i[0][-1] for i in return_list]

            match_scores_return = [pretty_percentages(match_scores_dict[i]) for i in result_idx]

            if not request.form.get('email'):
                email_id = 'NA'
            else:
                email_id = request.form.get('email')
            store_details = request.form.get('infostore') != None
            if not store_details:
                os.remove(f'./uploads/{filename}')
                cur.execute("INSERT INTO users(email_id, filename, can_contact) VALUES (?, 'No file', 0);", [email_id])
                con.commit()
                print('Info stored without resume')
            elif store_details:
                cur.execute('INSERT INTO users(email_id, filename, can_contact) VALUES (?, ?, 1);', [request.form.get('email'), filename])
                con.commit()
                print('Info stored with resume')
            print(type(request.form.get('infostore')))
            print(request.form.get('infostore'))

            return render_template('results.html', return_list=return_list, match_scores=match_scores_return, enumerate=enumerate, companies_list=companies_list, posn_list=posn_list, salary_list=salary_list, experience_list=experience_list, location_list=location_list, jd_list=jd_list, link_list=link_list)

        return redirect(request.url)

@app.route("/insights")
def insights():
    """Shows the insights page"""

    return render_template('insights.html')

@app.route("/about")
def about():
    """Shows the about page"""

    return render_template('about.html')
