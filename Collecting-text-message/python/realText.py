
import pandas as pd
from pymongo import MongoClient
import nltk #Natual Language Toolkit
import string #for list of punctuation
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
#from nltk.stem.porter import PorterStemmer
import matplotlib.pyplot as plt
pd.set_option('expand_frame_repr', False)
pd.set_option('display.width', 1000)
pd.set_option('display.max_rows', 50)
pd.set_option('max_colwidth', 200) 

client = MongoClient("mongodb+srv://dbBot:dbBot4343@cluster0.ahhgb.mongodb.net/test")
db = client["disBotDB"]

def textAna():
  text = db.disBotDB
  #convert entire collection to Pandas dataframe
  df = pd.DataFrame(list(text.find({})))

  print(df)

  #text pre-processing-------------------------------------------------------
  #remove punctuation
  def remove_punctuation(text):
      no_punct = "".join([c for c in text if c not in string.punctuation])
      return no_punct

  df['content'] = df['content'].apply(lambda x: remove_punctuation(x))
  #print("remove_punctuation")
  #print(df)

  #Tokenization -- beak down text paragraph into word list 
  #lowercase
  tokenizer = RegexpTokenizer('\w+')
  df['content'] = df['content'].apply(lambda x: tokenizer.tokenize(x.lower()))
  #print("tokenize")
  #print(df)
 
  #stopword
  nltk.download('stopwords')
  stopwords.words('english')
  #remove stopword
  #remove low predictive power in our small corpus
  def remove_stopwords(text):
      words = [w for w in text if w not in stopwords.words('english')]
      return words
  df['content'] = df['content'].apply(lambda x: remove_stopwords(x))


  #Lemmatizing
  nltk.download('wordnet')
  lemmatizer = WordNetLemmatizer()
  def word_lemmatizer(text):
      lem_text = " ".join([lemmatizer.lemmatize(w) for w in text])
      return lem_text
  df['content_lem'] = df['content'].apply(lambda x: word_lemmatizer(x))
  #print("lemmatizer")
  #print(df)

  df['content']=df['content_lem']
  df = df.iloc[:,:5]
  #deal with error
  #remove number

  #export postprocess to database 
  db2 = client['disBotDB']
  collection = db2['disBotDB_post']
  df.reset_index(inplace=True)
  data_dict = df.to_dict("records")
  # Insert collection
  collection.insert_many(data_dict)

