
import os
import numpy as np
import pandas as pd
from rake_nltk import Rake
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import nltk


APP_PATH = os.path.dirname(os.path.abspath(__file__))

netflix_data = pd.read_csv(os.path.join(
    APP_PATH, os.path.join("Dataset", "netflix_titles.csv")), index_col=False)

netflix_data.drop(['director','country','date_added','release_year','duration','Unnamed: 12','show_id','rating'],inplace=True,axis=1)


#netflix_data.isna().sum()

netflix_data.dropna(inplace=True)



netflix_data['Key_words'] = "" 
netflix_data['Type'] = "" 
for index, row in netflix_data.iterrows():
    description = row['description']
    r = Rake()
    r.extract_keywords_from_text(description)
    key_words_dict_scores = r.get_word_degrees()
    row['Key_words'] = list(key_words_dict_scores.keys())
    
netflix_data.drop(columns = ['description'], inplace = True)
 

netflix_data['listed_in'] = netflix_data['listed_in'].map(lambda x: x.lower().split(','))
netflix_data['cast'] = netflix_data['cast'].map(lambda x: x.split(',')[:3])
# netflix_data['director'] = netflix_data['director'].map(lambda x: x.split(','))
#netflix_data

netflix_data.set_index('title', inplace = True)
#netflix_data.head() 
    

netflix_data['bag_of_words'] = ''
columns = netflix_data.columns
for index, row in netflix_data.iterrows():
    words = ''
    for col in columns:
        if col != 'director':
            words = words + ' '.join(row[col])+ ' '
        else:
            words = words + row[col]+ ' '
    row['bag_of_words'] = words
    
netflix_data.drop(columns = [col for col in netflix_data.columns if col!= 'bag_of_words'], inplace = True)



#netflix_data.head()


count = CountVectorizer()
count_matrix = count.fit_transform(netflix_data['bag_of_words'])

indices = pd.Series(netflix_data.index)

cosine_sim = cosine_similarity(count_matrix, count_matrix)



def recommendations(Title, cosine_sim = cosine_sim):
    
    recommended_movies = []
    idx = indices[indices == Title].index[0]
    score_series = pd.Series(cosine_sim[idx]).sort_values(ascending = False)
    top_10_indexes = list(score_series.iloc[1:11].index)
    #score=list(score_series.iloc[1:11].values.round(1))
    
    dic_result={}
    for i in top_10_indexes:
        dic_result[netflix_data.index[i]]=score_series[i].round(1)
        
        #recommended_movies.append(list(netflix_data.index)[i])
    recommended_movies.append(dic_result)
    return recommended_movies


#print(recommendations('Rocky'))






