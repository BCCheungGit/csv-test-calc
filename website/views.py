from flask import Blueprint, render_template, flash, request, redirect, url_for
from flask_login import login_required, current_user
from .models import User
from . import db
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf



views = Blueprint('views', __name__)

@views.route('/')
@views.route('/home')
@login_required
def home():
    yfdata = yf.download('BTC-USD')
    yfdata.to_csv('btcprice.csv')
    btc_price_data = pd.read_csv('btcprice.csv',
                             index_col=False, 
                             low_memory=False,  
                             names=["Date", 
                                    "Open",
                                    "High",
                                    "Low",
                                    "Close",
                                    "Adj Close",
                                    "Volume"],
                                    skiprows=1)
    pricedata = btc_price_data.astype({'High': 'float', 'Low' : 'float'})
    high_price_mean = pricedata['High'].mean()
    high_price_median = pricedata['High'].median()
    high_price_std = pricedata['High'].std()
    
    low_price_mean = pricedata['Low'].mean()
    low_price_median = pricedata['Low'].median()
    low_price_std = pricedata['Low'].std()
    
    return render_template('home.html', user=current_user)