import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st
import matplotlib.pyplot as plt


def daily_most_user(df):
    daily_df = df.groupby(by="weekday").agg({
        "count": "sum"
    }).reset_index().sort_values(by="count", ascending=False)

    return daily_df

def monthly_most_user(df):
    monthly_df = df.groupby(by="month").agg({
        "count": "sum"
    }).reset_index().sort_values(by="count", ascending=False)

    return monthly_df

def yearly_most_user(df):
    yearly_df = df.groupby(by="year").agg({
        "count": "sum"
    }).reset_index()

    yearly_df['pct_change'] = yearly_df['count'].pct_change() * 100

    return yearly_df

def weather_most_user(df):
    weather_df = df.groupby(by="weathersit").agg({
        "count": "sum"
    }).reset_index().sort_values(by="count", ascending=False)

    return weather_df

def season_most_user(df):
    weather_df = df.groupby(by="season").agg({
        "count": "sum"
    }).reset_index().sort_values(by="count", ascending=False)

    return weather_df

def winspeed_group_df(df):
    windspeed_df = df.groupby(by='windspeed_category')['count'].sum().sort_values(ascending=False).reset_index()

    return windspeed_df