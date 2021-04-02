from newspaper import Article
import random
import string
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import warnings
warnings.filterwarnings('ignore')
nltk.download('punkt', quiet=True)


# Reading Article from website and downloading.
article = Article('https://en.wikipedia.org/wiki/Artificial_intelligence')
article.download()
article.parse()
article.nlp()
corpus = article.text

# Tockenizing the text.
text = corpus
sentence_list = nltk.sent_tokenize(text)

# Generating Greeting Response from user side and bot side.
def greething_response(text):
      text = text.lower()
      bot_greetings = ['how are you', 'hi', 'hai', 'hey', 'hello', 'whatsup']
      user_greetings = ['hi', 'hey', 'hello', 'hai', 'greetings', 'whatsup', 'fine']
      for word in text.split():
          if word in user_greetings:
              return random.choice(bot_greetings)

# Index vise sorting and getting more similar in first.
def index_sort(list_var):
    length = len(list_var)
    list_index = list(range(0, length))
    x = list_var
    for i in range(length):
        for j in range(length):
            if x[list_index[i]] > x[list_index[j]]:
                temp = list_index[i]
                list_index[i] = list_index[j]
                list_index[j] = temp
    return list_index

# Generating Bot responce by user input.
def bot_response(user_input):
    user_input = user_input.lower()
    sentence_list.append(user_input)
    bot_response = ''
    cm = CountVectorizer().fit_transform(sentence_list)
    similarity_score = cosine_similarity(cm[-1], cm)
    similarity_score_list = similarity_score.flatten()

    index = index_sort(similarity_score_list)
    index = index[1:]
    response_flag = 0
    j = 0
    # Cheking similarity score and the giving response to user. considering olny 2 prioritys
    for i in range(len(index)):
        if similarity_score_list[index[i]] > 0.0:
            bot_response = bot_response+' '+sentence_list[index[i]]
            response_flag = 1
            j += 1
            if j > 2:
                break

    # for Bad response from user.
    if response_flag == 0:
        bot_response = bot_response+' '+" Sorry, I don't understand"
      
    sentence_list.remove(user_input)
    return bot_response
  
# welcome note from Bot side
print('Bot: I am MasterAI Bot. I will answer your quries about Artificial intelligence (from wikipedia). \nif you want to exit, type bye/exit.')

# exiting words list
exit_list = ['exit', 'see you later', 'bye', 'quit', 'get lost']

while(True):
  user_input = input()
  if user_input.lower()in exit_list:
    print('MasterAI Bot Chat with you later')
    break
  else:
    if greething_response(user_input) != None:
      print('MasterAI Bot: '+greething_response(user_input))
    else:
      print('MasterAI Bot: '+bot_response(user_input))