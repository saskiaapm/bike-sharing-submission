import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='white')

day_df = pd.read_csv("/Bike Sharing Dataset/day_clean.csv")
day_df['date'] = pd.to_datetime(day_df['date'])
def create_daily_rent_df(df):
    daily_rent_df = df.groupby(by = 'date').agg({'total_count': 'sum'}).reset_index()
    return daily_rent_df

def create_daily_casual_rent_df(df):
    daily_casual_rent_df = df.groupby(by='date').agg({'casual': 'sum'}).reset_index()
    return daily_casual_rent_df

def create_daily_registered_rent_df(df):
    daily_registered_rent_df = df.groupby(by = 'date').agg({'registered': 'sum'}).reset_index()
    return daily_registered_rent_df
  
def create_season_rent_df(df):
    season_rent_df = df.groupby(by = 'season').agg({'total_count': 'sum'}).reset_index()
    return season_rent_df

def create_monthly_rent_df(df):
    monthly_rent_df = df.groupby(by = 'month').agg({'total_count': 'sum'})
    ordered_months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    monthly_rent_df = monthly_rent_df.reindex(ordered_months, fill_value=0)
    return monthly_rent_df

def create_weekday_rent_df(df):
    weekday_rent_df = df.groupby(by = 'day').agg({'total_count': 'sum'}).reset_index()
    return weekday_rent_df

def create_workingday_rent_df(df):
    workingday_rent_df = df.groupby(by = 'workingday').agg({'total_count': 'sum'}).reset_index()
    return workingday_rent_df

def create_weather_rent_df(df):
    weather_rent_df = df.groupby(by = 'weather').agg({'total_count': 'sum'})
    return weather_rent_df

def create_rfm_df(df):
    rfm_df = df.groupby(by = "day", as_index = False).agg({
        "date" : "max",
        "instant" : "nunique",
        "total_count" : "sum"
    })
    rfm_df.columns = ["day", "max_order_timestamp", "frequency", "monetary"]
    rfm_df["max_order_timestamp"] = rfm_df["max_order_timestamp"].dt.date
    recent_date = day_df["date"].dt.date.max()
    rfm_df["recency"] = rfm_df["max_order_timestamp"].apply(lambda x: (recent_date - x).days)
    rfm_df.drop("max_order_timestamp", axis = 1, inplace = True)
    return rfm_df



min_date = pd.to_datetime(day_df['date']).dt.date.min()
max_date = pd.to_datetime(day_df['date']).dt.date.max()

with st.sidebar:
    st.image("https://images.vexels.com/media/users/3/265753/isolated/preview/d42c21d6511cb6717baf33918df1605f-bike-retro-transport-vehicle.png")
    start_date, end_date = st.date_input(
        label = 'Select Date (Start Date and End Date)',
        min_value = min_date,
        max_value = max_date,
        value = [min_date, max_date])

main_df = day_df[(day_df['date'] >= str(start_date)) & (day_df['date'] <= str(end_date))]

daily_rent_df = create_daily_rent_df(main_df)
daily_casual_rent_df = create_daily_casual_rent_df(main_df)
daily_registered_rent_df = create_daily_registered_rent_df(main_df)
season_rent_df = create_season_rent_df(main_df)
monthly_rent_df = create_monthly_rent_df(main_df)
weekday_rent_df = create_weekday_rent_df(main_df)
workingday_rent_df = create_workingday_rent_df(main_df)
weather_rent_df = create_weather_rent_df(main_df)
rfm_df = create_rfm_df(main_df)


st.header('Bike Rental Dashboard🚲')
st.subheader('Daily Rentals')
col1, col2, col3 = st.columns(3)

with col1:
  daily_rent_casual = daily_casual_rent_df['casual'].sum()
  st.metric('Casual User', value = daily_rent_casual)

with col2:
  daily_rent_registered = daily_registered_rent_df['registered'].sum()
  st.metric('Registered User', value = daily_rent_registered)

with col3:
  daily_rent_total = daily_rent_df['total_count'].sum()
  st.metric('Total User', value = daily_rent_total)

fig, ax = plt.subplots(figsize = (16, 8))
ax.plot(
    daily_rent_df["date"],
    daily_rent_df["total_count"],
    marker = 'o', 
    linewidth = 2,
    color = "#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
 
st.pyplot(fig)

st.subheader('Monthly Rentals')
fig, ax = plt.subplots(figsize = (24, 8))
ax.plot(
    monthly_rent_df.index,
    monthly_rent_df['total_count'],
    marker = 'o', 
    linewidth = 2,
    color = "#90CAF9")

for index, row in enumerate(monthly_rent_df['total_count']):
    ax.text(index, row + 1, str(row), ha = 'center', va = 'bottom', fontsize = 12)

ax.tick_params(axis = 'x', labelsize = 25, rotation = 45)
ax.tick_params(axis = 'y', labelsize = 20)
st.pyplot(fig)

st.subheader("Number of Users by Weather and Season")

col1, col2 = st.columns(2)
 
with col1:
    fig, ax = plt.subplots(figsize = (20, 10))
    colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
    sns.barplot(
        y = "total_count", 
        x = "weather",
        data = weather_rent_df.sort_values(by = "total_count", ascending = False),
        palette=colors,
        ax=ax
    )
    ax.set_title("Number of Customer by Weather", loc = "center", fontsize = 50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis = 'x', labelsize = 35)
    ax.tick_params(axis = 'y', labelsize = 30)
    st.pyplot(fig)
fig, ax = plt.subplots(nrows = 1, ncols = 2, figsize = (35, 15))
with col2:
    fig, ax = plt.subplots(figsize=(20, 10))
    colors = ["#D3D3D3", "#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
    sns.barplot(
        y = "total_count", 
        x = "season",
        data = season_rent_df.sort_values(by = "season", ascending = False),
        palette = colors,
        ax = ax
    )
    ax.set_title("Number of Customer by Season", loc = "center", fontsize = 50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis = 'x', labelsize = 35)
    ax.tick_params(axis = 'y', labelsize = 30)
    st.pyplot(fig)

st.subheader("Best Customer Based on RFM Parameters (day)")
col1, col2, col3 = st.columns(3)

with col1:
    avg_recency = round(rfm_df.recency.mean(), 1)
    st.metric("Average Recency (days)", value = avg_recency)

with col2:
    avg_frequency = round(rfm_df.frequency.mean(), 2)
    st.metric("Average Frequency", value = avg_frequency)

with col3:
    avg_monetary = format_currency(rfm_df.monetary.mean(), "AUD", locale='es_CO') 
    st.metric("Average Monetary", value = avg_monetary)

fig, ax = plt.subplots(nrows = 1, ncols = 3, figsize = (35, 15))
colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(y = "recency", x = "day", data = rfm_df.sort_values(by = "recency", ascending = True).head(5), palette = colors, hue = "day", legend = False, ax = ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("By Recency (days)", loc="center", fontsize=50)
ax[0].tick_params(axis = 'y', labelsize = 25)
ax[0].tick_params(axis = 'x', labelsize = 30, rotation = 45)

sns.barplot(y = "frequency", x = "day", data = rfm_df.sort_values(by = "frequency", ascending = False).head(5), palette = colors, hue = "day", legend = False, ax = ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].set_title("By Frequency", loc = "center", fontsize = 50)
ax[1].tick_params(axis = 'y', labelsize = 25)
ax[1].tick_params(axis = 'x', labelsize = 30, rotation = 45)

sns.barplot(y = "monetary", x = "day", data = rfm_df.sort_values(by = "monetary", ascending = False).head(5), palette = colors, hue = "day", legend = False, ax = ax[2])
ax[2].set_ylabel(None)
ax[2].set_xlabel(None)
ax[2].set_title("By Monetary", loc = "center", fontsize = 50)
ax[2].tick_params(axis = 'y', labelsize = 25)
ax[2].tick_params(axis = 'x', labelsize = 30, rotation = 45)

st.pyplot(fig)

st.caption('Copyright (c) Saskia Putri Maharani 2024')