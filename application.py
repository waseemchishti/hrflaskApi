# pip3 install PyPDF2
# pip install textract
# pip install nltk
# pip install docx2txt
#pip install fuzzywuzzy
import nltk
nltk.download('punkt')
#spacy
import spacy
# from spacy.pipeline import EntityRuler
# from spacy.lang.en import English
# from spacy.tokens import Doc

#gensim
# import gensim
# from gensim import corpora

#Visualization
from spacy import displacy
# import pyLDAvis.gensim_models
# from wordcloud import WordCloud
# import plotly.express as px
import matplotlib.pyplot as plt

#Data loading/ Data manipulation
import pandas as pd
import numpy as np
import jsonlines
import os
#nltk
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
nltk.download(['stopwords','wordnet'])

#warning
import warnings 
warnings.filterwarnings('ignore')
import PyPDF2 
import textract
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import docx2txt as dtxt
import pandas as pd
import re
# !pip install pdfminer
import os
# position='ENGINEERING''
# from docx import *
import spacy

#Build upon the spaCy Small Model
nlp = spacy.load("en_core_web_sm")



#Create the EntityRuler
ruler = nlp.add_pipe("entity_ruler")

from flask import Flask, redirect, url_for, request, render_template,make_response, send_file,jsonify
from json2html import *
from IPython.display import HTML
sys.setrecursionlimit(10**6)
import json
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
import numpy as np
import re
from io import BytesIO
import pyodbc
import jinja2
import string
punct =  string.punctuation
punct=list(punct)
punct.remove('|')
import glob
import PyPDF2
# import fitz
from pdfminer.high_level import extract_text
from pdfminer.high_level import extract_text
from importlib import reload
from EntitiesExtraction_module1 import *
import EntitiesExtraction_module1 as mod1
from EntitiesExtraction_module2 import *
import EntitiesExtraction_module2 as mod2
reload(mod1)
reload(mod2)
#read dataset
# city.head()
uni=pd.DataFrame(pd.read_csv("world_universities.csv"))
# print(uni.head())
country=pd.DataFrame(pd.read_excel("cities500.xlsx"))
city=pd.DataFrame(pd.read_excel("cities500.xlsx"))



app = Flask(__name__)

import werkzeug
import ssl
# flask_app = Flask( __name__)

@app.route('/')
def index():
    return ("--Hello word--")
    
@app.route('/Resume_segmentation/<path:urls>/<skills>', methods=['GET','POST'])
def read_resume(urls, skills):
    #-------------------------------------------------------------------------------------------------------------
    def extract_text_from_pdf(pdf_path):

        return extract_text(pdf_path)

    def read_files(file_path):  
        import glob
        resumes=[]

#         print(os.chdir("*"))
        for file in glob.glob(file_path+'/*'):
            print(file)
            if file.endswith('.pdf'):
                resumes.append(extract_text_from_pdf(file))

            elif file.endswith('.docx'):
                text=dtxt.process(file)
    #         file.endswith('.docx'):
                resumes.append(text)
        return resumes
    #-----------------------------------------------------------------------------------------------------------------
    file_path = urls
    skills_list = skills
    skills_list=skills_list.split(",")
#................................................................................
    resumes=read_files(file_path)
    data=pd.DataFrame(list(resumes), columns=['Resumes'])
    result=mod1.module_1_entities(data,uni,country,city)
    
    
    for a in range(len(result)):
    
        result['City'][a]=list(dict.fromkeys(result['City'][a]))
        result['Location'][a]=list(dict.fromkeys(result['Location'][a]))
        result['University'][a]=list(dict.fromkeys(result['University'][a]))
        result['Contact'][a]=list(dict.fromkeys(result['Contact'][a]))
        result['Email'][a]=list(dict.fromkeys(result['Email'][a]))
        result['URLS'][a]=list(dict.fromkeys(result['URLS'][a]))
        
    length1=len(result)
    result2=mod2.best_Match_resume(data,skills_list)
#     length2=len(result2)
#     result['Date']=""
#     result['Summary']=""
#     result['NewSkills']=""
#     result['match_Item']=""
#     result['match_Item_Count']=""
#     result['Date']=result2['Date']
#     result['Summary']=result2['summary']
#     result['NewSkills']=result2['NewSkills']
#     result['match_Item']=result2['match_Item']
#     result['match_Item_Count']=result2['match_Item_Count']
    print(result)
#     print(result2)
#     result3=result.merge(result2, how='left')
    result=result.to_json()
#     result3=result2.to_json()
    
#     result3=HTML(df.to_html(classes='table table-stripped'))
    
#     json_data = jsonify(trails=result),{'Content-Type':'application/json'}
    return result
#     return json2html.convert(json=json_data)
#     os.chdir(r"C:\Users\WaseemAhmad\extraViz\spacy\flaskapi")
#     workingdir = os.path.abspath(os.getcwd())
#     print(workingdir)
#     return render_template("resumes_module1.html", dic=result, length1=length1,length2=length2,dic2=result2)
#..........................................................................................................    
# @app.route('/Resume_segmentation_module2',methods = ['POST', 'GET'])
# def resume_segmentation2():
    

if __name__ == '__main__':
    app.run(port=5000)
