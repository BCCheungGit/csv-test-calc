from flask import Blueprint, render_template, flash, request, redirect, url_for
from flask_login import login_required, current_user
from .models import User
from . import db
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from pathlib import Path
from bs4 import BeautifulSoup as Soup
import glob

views = Blueprint('views', __name__)

@views.route('/')
@views.route('/upload')
@login_required
def upload():
    #yfdata = yf.download('BTC-USD')
    #yfdata.to_csv('btcprice.csv')
    #btc_price_data = pd.read_csv('btcprice.csv',
    #                         index_col=False, 
    #                         low_memory=False,  
    #                         names=["Date", 
    #                                "Open",
    #                                "High",
    #                                "Low",
    #                                "Close",
    #                                "Adj Close",
    #                                "Volume"],
    #                                skiprows=1)
    #filepath = r"C:\Users\Benjamin Cheung\projects\csv-test-calc\btcprice.csv"
    
    #filename=Path(filepath).name
    return render_template('upload.html', user=current_user)

@views.route('/success', methods=['POST'])
def fileupload():
    if request.method == 'POST':
        f = request.files['file']
        f.save(f.filename)
        
        #filepath = Path(r"C:\Users\Benjamin Cheung\projects\csv-test-calc", f.filename)
        filedataframe = pd.read_csv(f.filename)
        smallerdf = pd.DataFrame(data=filedataframe.head(10))
        
        home_path = Path(r"C:\Users\Benjamin Cheung\projects\csv-test-calc\website\templates\home.html")
        soup = Soup(open(home_path), 'html5lib')
        
        h4 = soup.find('h4')
        print(smallerdf.to_html())
        h4.insert_after(smallerdf.to_html())
        
        return render_template('home.html', name=f.filename, user=current_user)
    