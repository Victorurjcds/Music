# -*- coding: utf-8 -*-
"""
Editor de Spyder

Tratamiento de textos en formato pdf.
"""


#from lightfm import LightFM


# My own:
import os
os.chdir('C:/Users/Victor/Documents/Ambito_profesional/proyectos/recommender_systems/music')
import pandas as pd
from scipy.spatial.distance import cosine

data = pd.read_csv('music.csv')
df = data.copy()
df = df.drop('user',1)
nans = df.isnull().values.any()

# Create a placeholder dataframe listing item vs. item
item_matrix = pd.DataFrame(index=df.columns,columns=df.columns)

# Lets fill in those empty spaces with cosine similarities
# Loop through the columns
for i in range(0,len(item_matrix.columns)) :
    # Loop through the columns for each column
    for j in range(0,len(item_matrix.columns)) :
      # Fill in placeholder with cosine similarities
      item_matrix.ix[i,j] = 1-cosine(df.ix[:,i],df.ix[:,j])



# Create a placeholder items for closes neighbours to an item:
data_neighbours = pd.DataFrame(index=item_matrix.columns,columns=range(1,12))
 
# Loop through our similarity dataframe and fill in neighbouring item names
for i in range(0,len(item_matrix.columns)):
    data_neighbours.ix[i,:11] = item_matrix.ix[0:,i].order(ascending=False)[:11].index

del data_neighbours[1] 
# --- End Item Based Recommendations --- #


###############################################################################
# Applied to each users:
def getScore(history, similarities):
   return sum(history*similarities)/sum(similarities)

data_sims = pd.DataFrame(0, index=data.index,columns=data.columns)
data_sims.ix[:,:1] = data.ix[:,:1]

#Loop through all rows, skip the user column, and fill with similarity scores
for i in range(0,len(data_sims.index)):
    for j in range(1,len(data_sims.columns)):
        user = data_sims.index[i]
        product = data_sims.columns[j]
        product_top_names = data_neighbours.ix[product]
        user_purchases = df.ix[user,product_top_names]
        
        if data.ix[i,j] != 1 and user_purchases.sum() > 0:      # Note that we score items that the user has already consumed as 0, because there is no point recommending it again.    
            product_top_sims = item_matrix.ix[product].order(ascending=False)[1:11]
            
            data_sims.ix[i,j] = getScore(user_purchases,product_top_sims)

# Get the top songs
data_recommend = pd.DataFrame(index=data_sims.index, columns=['user','1','2','3','4','5','6','7','8','9','10'])
data_recommend.ix[:,0] = data_sims.ix[:,0]
for i in range(0,len(data_sims.index)):
    data_recommend.ix[i,1:] = data_sims.ix[i,:].order(ascending=False).ix[1:11].index.transpose()


print (data_recommend.ix[:10,:4])


## Save:
data_recommend.to_excel('recommender_system.xlsx')
df.to_excel('dataset.xlsx')






