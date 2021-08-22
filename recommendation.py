# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import json
from sklearn.metrics.pairwise import cosine_similarity


def read_data():
    data_folder="./recommendation_data/"
    with open(data_folder+"events.json", "r") as read_file:
        event_data = json.load(read_file)
    with open(data_folder+"meta.json", "r",encoding="utf8") as meta_file:
        met_data = json.load(meta_file)
    events=pd.DataFrame(data=event_data['events'])
    meta=pd.DataFrame(data=met_data['meta'])
    evnt=events.iloc[0:50000]
    
    #Merge two datasets
    joined_df=pd.merge(evnt,meta,how='inner', on = 'productid')
    
    return joined_df

def find_products(id):
    df_join=read_data()
    recommended_products={}
    
    #pivot-table creation
    product_pivot = pd.pivot_table(df_join,index = 'sessionid',columns = 'productid',values = 'category',aggfunc = 'count')
    product_pivot.reset_index(inplace=True)
    product_pivot = product_pivot.fillna(0)
    product_pivot = product_pivot.drop('sessionid', axis=1)
    
    #co-occurence matrix for bought-together items
    co_occurence = product_pivot.T.dot(product_pivot)
    np.fill_diagonal(co_occurence.values, 0)
    
    #Cosine similarity calculation
    similarity_df = pd.DataFrame(cosine_similarity(co_occurence))
    similarity_df.index = co_occurence.index
    similarity_df.columns = np.array(co_occurence.index)
    
    #Searching 10 similar products
    ten_products = []
    for i in similarity_df.index:
        ten_products.append(similarity_df[similarity_df.index!=i][i].sort_values(ascending = False)[0:10].index)
    
    ten_products_df = pd.DataFrame(ten_products)     
    ten_products_df.index = similarity_df.index
    recommended_product = pd.merge(ten_products_df, df_join, on="productid")
    print(recommended_product.head())
    for j in range(0,9):
        
            recommended_products[ten_products_df[j][id]]={'name':recommended_product.name.values[np.where(recommended_product.productid==ten_products_df[j][id])],'price':recommended_product.price.values[np.where(recommended_product.productid==ten_products_df[j][id])]}
    
    
    rp=pd.DataFrame.from_dict(data=recommended_products)
    return rp.to_json(force_ascii=False).encode('utf-8')

    

    