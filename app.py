# -*- coding: utf-8 -*-
"""
Created on Sun Aug 22 13:15:31 2021

@author: akyol
"""

from flask import Flask, render_template,request
import recommendation
app = Flask(__name__)
@app.route('/products',methods = ['GET'])
def get_product():
    print("product_id: " + str('SGPAN971540'))
    
    return recommendation.find_products('SGPAN971540')
    
if __name__ == '__main__':
    
    app.run(host='localhost',port=5004)