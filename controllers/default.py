# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

import requests
import pandas as pandas
import numpy as np
from sklearn import datasets, linear_model
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures

@auth.requires_login()
def index():
    projection_date = None
    if request.post_vars:
        projection_date = request.vars.projection_date
    return dict(projection_date = projection_date)

def process_data(data):
    data = data.json()
    #del data[-1]
    #del data[-1]
    #data.append({"Country":"Guatemala","CountryCode":"GT","Province":"","City":"","CityCode":"","Lat":"15.78","Lon":"-90.23","Confirmed":557,"Deaths":16,"Recovered":62,"Active":0,"Date":"2020-04-28T00:00:00Z"})
    #data.append({"Country":"Guatemala","CountryCode":"GT","Province":"","City":"","CityCode":"","Lat":"15.78","Lon":"-90.23","Confirmed":557,"Deaths":16,"Recovered":62,"Active":0,"Date":"2020-04-29T00:00:00Z"})
    return data

@auth.requires_login()
def data():
    print('\n'*10)
    import datetime
    today_date = datetime.datetime.today()
    today = today_date.strftime('%Y-%m-%d')
    projection_date = datetime.datetime.strptime(request.vars.projection_date, '%Y-%m-%d')
    start_date = datetime.datetime.strptime('2020-03-14', '%Y-%m-%d') - datetime.timedelta(days=1)
    days = (projection_date.date() - today_date.date()).days +  ( today_date.date() - start_date.date()).days
    print(days)
    print(( today_date.date() - start_date.date()).days)

    data = requests.get('https://api.covid19api.com/country/guatemala?from=2020-03-14T00:00:00Z&to=%sT00:00:00Z' %(today))
    data = process_data(data)
    list_confirmed = []
    list_deaths    = []
    list_recovered = []
    list_dates     = []
    for element in data:
        list_confirmed.append(element["Confirmed"])
        list_deaths.append(element["Deaths"])
        list_recovered.append(element["Recovered"] )
        list_dates.append(element["Date"].replace('T00:00:00Z','').replace('2020-','') )
        

    covid_df = pandas.DataFrame.from_dict(data)
    covid_df['Days'] = range(0, len(covid_df))
    x = covid_df[['Days']]
    

    confirmed, model_confirmed = get_ec_and_total(x,covid_df[['Confirmed']], days)
    deaths, model_deaths = get_ec_and_total(x,covid_df[['Deaths']], days)
    recovered, model_recovered = get_ec_and_total(x,covid_df[['Recovered']], days)
    def get_percentage(part, whole):
        return 100 * float(part)/float(whole)
    return dict(model_confirmed = model_confirmed,
                model_deaths    = model_deaths,
                model_recovered = model_recovered,
                confirmed       = confirmed,
                deaths          = deaths,
                recovered       = recovered,
                total_confirmed = covid_df['Confirmed'].iloc[-1],
                total_deaths    = covid_df['Deaths'].iloc[-1],
                total_recovered = covid_df['Recovered'].iloc[-1],
                list_confirmed  = list_confirmed,
                list_deaths     = list_deaths, 
                list_recovered  = list_recovered,
                list_dates      = list_dates,
                get_percentage  = get_percentage,
                population      = 18000000 )



def get_ec_and_total(x,y, days):

    x_train, x_test_, y_train, y_test = train_test_split(x, y, test_size=0.2)

    poli_reg = PolynomialFeatures(degree = 2)

    x_train_poli = poli_reg.fit_transform(x_train)
    x_test_poli = poli_reg.fit_transform(x_test_)

    pr = linear_model.LinearRegression()
    pr.fit(x_train_poli, y_train)
    Y_pred_pr = pr.predict(x_test_poli)

    coef = pr.coef_[0]
    constant = pr.intercept_

    model_presition = pr.score(x_train_poli, y_train)

    import sympy
    x = sympy.symbols('x')
    y = '%f*x + %f*x*x + %f' %(coef[1],coef[2],constant)
    e = sympy.simplify(y).subs(x,days)
    return ( int(e), replace_x(y)  )


def replace_x(model):
    return model.replace('*x*x', 'x^2').replace('*x', 'x')

# ---- Action for login/register/etc (required for auth) -----
def user():
    if request.args(0)=='login':
        redirect(URL('default','login'))
    return dict(form=auth())

def login():
    form=auth.login()
    return dict(form = form)
