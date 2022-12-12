
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



  #print("remove_stopwords")
  #print(df)

  #back to root word/ cut prefix and ending 
  #stemming --- can lose its actual meaning
  # stemmer = PorterStemmer()
  # def word_stemmer(text):
  #     stem_text = [stemmer.stem(w) for w in text]
  #     return stem_text
  # df['content_stem'] = df['content'].apply(lambda x: word_stemmer(x))
  # print("word_stemmer")
  # print(df) 

  # #text analysis-------------------------------------------------------
  # #Term frequency
  # tf1 = (df['content']).apply(lambda x: pd.value_counts(x.split(" "))).sum(axis = 0).reset_index()
  # tf1.columns = ['words','tf']
  # #pd.set_option('display.max_rows', None)
  # tf1=tf1.sort_values(by=['tf'],ascending=False)
  # tf1Top = tf1.nlargest(15, 'tf')
 
  # #wordcolud
  # import re
  # contents = ((str(df['content'].tolist())))
  # contentsList = re.sub("[^\w]", " ",  contents).split()

  # # Plot horizontal bar graph
  # fig, axes = plt.subplots(1,2,figsize=(15, 8),gridspec_kw={'width_ratios': [1, 2]})
  # tf1Top.sort_values(by='tf').plot.barh(x='words',
  #                       y='tf',
  #                       ax=axes[0],
  #                       color="purple")

  # axes[0].set_title("15 Most Frequently Occuring words")
  # axes[0].set_ylabel('Word')
  # axes[0].set_xlabel('Occurances')

  # from wordcloud import WordCloud
  # wordcloud = WordCloud(max_font_size=100, max_words=100, background_color="white",width=400).generate(contents)
  # axes[1].imshow(wordcloud, interpolation='bilinear')
  # axes[1].axis("off")
  # plt.show()

  # #profanity check