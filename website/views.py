from flask import Blueprint, render_template, flash, request, redirect, url_for
from flask_login import login_required, current_user
from .models import User
from . import db
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from pathlib import Path

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
    filepath = r"C:\Users\Benjamin Cheung\projects\csv-test-calc\btcprice.csv"
    

    return render_template('home.html', user=current_user, filename=Path(filepath).name)