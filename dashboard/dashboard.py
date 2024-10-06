from visual_group import *

# Konfigurasi halaman
st.set_page_config(page_title="Dashboard Analisis", layout="wide")

# Menambahkan judul dan subjudul dengan desain lanjutan yang lebih estetik, minimalis, dan berfokus pada tampilan gelap
st.markdown(
    """
    <style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    /* Styling untuk keseluruhan halaman - dark mode */
    .reportview-container {
        background: radial-gradient(circle, rgba(33,33,33,1) 0%, rgba(18,18,18,1) 100%);
        color: #f0f0f0;
        font-family: 'Inter', sans-serif;
    }

    /* Gaya untuk judul utama */
    .main-title {
        font-size: 3.2em;
        font-weight: 700;
        background: linear-gradient(90deg, rgba(29,185,84,1) 0%, rgba(5,117,230,1) 100%);
        -webkit-background-clip: text;
        color: transparent;
        text-align: center;
        margin: 0 0 0 20px;
        letter-spacing: 1px;
    }

    /* Gaya untuk subjudul */
    .sub-title {
        font-size: 1.4em;
        font-weight: 400;
        color: #bbb;
        text-align: center;
        margin-top: -10px;
    }

    /* Kontainer utama judul */
    .header-container {
        background-color: #222;
        padding: 40px;
        border-radius: 10px;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.6);
        transition: all 0.3s ease;
    }

    /* Efek hover pada kontainer */
    .header-container:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.8);
    }

    /* Gaya untuk elemen sidebar */
    .sidebar-title {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        font-size: 1.5em;
        margin-bottom: 10px;
    }

    /* Styling link atau elemen interaktif */
    .st-a {
        color: #1db954;
        text-decoration: none;
    }

    .st-a:hover {
        color: #1d75b9;
        text-decoration: underline;
    }

    /* Animasi fade-in untuk judul */
    @keyframes fadeIn {
        0% { opacity: 0; }
        100% { opacity: 1; }
    }
    </style>
    
    <div class="header-container">
        <h1 class="main-title">Analisis Data - Bike Sharing</h1>
        <p class="sub-title">oleh Diaz Islami</p>
    </div>
    <br>
    """, 
    unsafe_allow_html=True
)

# Membaca dataset secara langsung tanpa unggah file
hour_df = pd.read_csv("dashboard/main_data1.csv")
day_df = pd.read_csv("dashboard/main_data2.csv")

st.sidebar.subheader("Tinjauan Data")

expand_data1 = st.sidebar.expander("Data Pertama", expanded=True)
expand_data1.write(hour_df.head())

expand_data2 = st.sidebar.expander("Data Kedua", expanded=True)
expand_data2.write(day_df.head())

st.sidebar.subheader("Pilih Filter Performa")

# Input rentang jam untuk filterisasi data
expand_filter = st.sidebar.expander("Filter Data", expanded=True)

user_options = ['count', 'casual', 'registered']
selected_users = expand_filter.selectbox("Pilih jenis pengguna", user_options)

min_hour, max_hour = expand_filter.slider("Pilih rentang jam", 0, 23, (0, 23))

# Filterisasi berdasarkan jam jika kolom 'hour' ada
if 'hour' in hour_df.columns:
    hour_df_filtered = hour_df[(hour_df['hour'] >= min_hour) & (hour_df['hour'] <= max_hour)].drop('instant', axis=1)
else:
    expand_filter.warning("Kolom 'hour' tidak ditemukan. Data tidak dapat difilter berdasarkan jam.")
    hour_df_filtered = hour_df  # Tidak difilter jika kolom 'hour' tidak ada

# Elemen selectbox untuk memilih cuaca, musim, dan hari
# Filter cuaca jika kolom 'weathersit' ada
if 'weathersit' in hour_df.columns:
    weather_options = ['Semua'] + hour_df['weathersit'].unique().tolist()  # Tambahkan opsi 'Semua'
    selected_weather = expand_filter.selectbox("Pilih kondisi cuaca", weather_options)
    if selected_weather != 'Semua':
        hour_df_filtered = hour_df_filtered[hour_df_filtered['weathersit'] == selected_weather]

# Filter musim jika kolom 'season' ada
if 'season' in hour_df.columns:
    season_options = ['Semua'] + hour_df['season'].unique().tolist()  # Tambahkan opsi 'Semua'
    selected_season = expand_filter.selectbox("Pilih musim", season_options)
    if selected_season != 'Semua':
        hour_df_filtered = hour_df_filtered[hour_df_filtered['season'] == selected_season]

# Filter hari jika kolom 'weekday' ada
if 'weekday' in hour_df.columns:
    weekday_options = ['Semua'] + hour_df['weekday'].unique().tolist()  # Tambahkan opsi 'Semua'
    selected_weekday = expand_filter.selectbox("Pilih hari", weekday_options)
    if selected_weekday != 'Semua':
        hour_df_filtered = hour_df_filtered[hour_df_filtered['weekday'] == selected_weekday]

# Filter hari jika kolom 'month' ada
if 'month' in hour_df.columns:
    month_options = ['Semua'] + hour_df['month'].unique().tolist()  # Tambahkan opsi 'Semua'
    selected_month = expand_filter.selectbox("Pilih bulan", month_options)
    if selected_month != 'Semua':
        hour_df_filtered = hour_df_filtered[hour_df_filtered['month'] == selected_month]

# Filter tren yang ditampilkan pada grafik
options = ['None', 'weathersit', 'season', 'weekday', 'month']
selected_opt = expand_filter.selectbox("Berdasarkan:", options)

# Menampilkan tabs untuk visualisasi
tab1, tab2, tab3 = st.tabs([
    "📊 Visualisasi Performa", 
    "📈 Visualisasi Rasio", 
    "🔍 Korelasi Fitur"
])

# Tab Deskripsi Data
with tab1:
    st.header("Performa Peminjaman")
    st.write("Jumlah baris dan kolom setelah filterisasi:", hour_df_filtered.shape)
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        total_orders = hour_df_filtered["count"].sum()
        st.metric(f"Total {selected_users.capitalize()} Users", value=total_orders)
    
    with col2:
        windspeed_mean = str(round(hour_df_filtered.windspeed.mean(), 2))
        st.metric("Windspeed Average", value=(windspeed_mean + " m/s"))

    with col3:
        humidity_mean = str(round(hour_df_filtered.humidity.mean(), 2))
        st.metric("Humidity Average", value=(humidity_mean + " %"))
    
    with col4:
        temp_mean = str(round(hour_df_filtered.temp.mean(), 2))
        st.metric("Temperature Average", value=(temp_mean + " °C"))
    
    if selected_opt != 'None':
        fig, ax = plt.subplots()
        if selected_users != 'count':
            sns.pointplot(data=hour_df_filtered, x='hour', y=selected_users, hue=selected_opt, ax=ax)
        else:
            sns.pointplot(data=hour_df_filtered, x='hour', y=selected_users, hue=selected_opt, ax=ax)
        plt.title(f"Count of Bikes per Hour by {selected_opt.capitalize()}", loc="center", fontsize=12)
        plt.xlabel("Hours")
        plt.ylabel("Total Rentals")
        plt.tick_params(axis='x', labelsize=8)
        st.pyplot(fig)
    else:
        fig, ax = plt.subplots()
        sns.pointplot(data=hour_df_filtered, x='hour', y='count', ax=ax)
        plt.title(f"Count of Bikes per Hour by {selected_opt.capitalize()}", loc="center", fontsize=12)
        plt.xlabel("Hours")
        plt.ylabel("Total Rentals")
        plt.tick_params(axis='x', labelsize=8)
        st.pyplot(fig)

# Tab Visualisasi Distribusi
with tab2:

    # pivot tabel hasil analisis yang ingin divisualisasikan
    daily_most_users = daily_most_user(day_df)
    monthly_most_users = monthly_most_user(day_df)
    yearly_most_users = yearly_most_user(day_df)
    weather_most_users = weather_most_user(day_df)
    season_most_users = season_most_user(day_df)
    windspeed_most_users = winspeed_group_df(hour_df)

    col1, col2 = st.columns(2)

    with col1:
        max_users = daily_most_users["count"][0]
        st.metric(f"Total Bike Rentals in {daily_most_users['weekday'][0]}", value=max_users)
        fig, ax1 = plt.subplots(figsize=(10,8))
        colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
        sns.barplot(
            x="count", 
            y="weekday",
            data=daily_most_users,
            palette=colors,
            ax=ax1
        )
        ax1.set_title("Total Bike Rentals per Day", loc="center", fontsize=20)
        ax1.set_ylabel(None)
        ax1.set_xlabel(None)
        ax1.tick_params(axis='y', labelsize=15)
        ax1.tick_params(axis='x', labelsize=15)
        st.pyplot(fig)
    
    with col2:
        max_users = monthly_most_users["count"].max()
        st.metric(f"Total Users in {monthly_most_users['month'][1]}", value=max_users)
        fig, ax2 = plt.subplots(figsize=(10,7.77))
        colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
        sns.barplot(
            x="count", 
            y="month",
            data=monthly_most_users.head(7),
            palette=colors,
            ax=ax2
        )
        ax2.set_title("Total Bike Rentals per Month", loc="center", fontsize=20)
        ax2.set_ylabel(None)
        ax2.set_xlabel(None)
        ax2.tick_params(axis='y', labelsize=15)
        ax2.tick_params(axis='x', labelsize=15)
        st.pyplot(fig)

    col3, col4 = st.columns(2)

    with col3:
        max_users = yearly_most_users["count"].sum()
        st.metric(f"Total Bike Rentals by Year", value=max_users)
        fig, ax3 = plt.subplots(figsize=(10,8))
        ax3.bar(yearly_most_users['year'], yearly_most_users['count'], color=["#D3D3D3", "#90CAF9"])
        ax3.set_title("Total Bike Rentals per Year", loc="center", fontsize=20)
        ax3.set_xlabel("Year")
        ax3.set_ylabel("Total Users")
        ax3.set_xticks([2011, 2012])
        st.pyplot(fig)
    
    with col4:
        latest_year = yearly_most_users['year'].max()
        latest_pct_change = str(round(yearly_most_users.loc[yearly_most_users['year'] == latest_year, 'pct_change'].values[0], 2))
        st.metric("Percentage Change by Year", value=(latest_pct_change+'%'))
        fig, ax4 = plt.subplots(figsize=(10,7.77))
        ax4.pie(yearly_most_users['count'], labels=yearly_most_users['year'], autopct='%1.1f%%', colors=["#D3D3D3", "#90CAF9"])
        ax4.set_title("Distribution of Bike Rentals by Year", loc="center", fontsize=20)
        st.pyplot(fig)

    col5, col6 = st.columns(2)

    with col5:
        max_users = season_most_users["count"][0]
        st.metric(f"Total Users in {season_most_users['season'][0]}", value=max_users)
        fig, ax5 = plt.subplots(figsize=(10,7.7))
        colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
        sns.barplot(
            y="count", 
            x="season",
            data=season_most_users,
            palette=colors,
            ax=ax5
        )
        ax5.set_title("Total Bike Rentals per Season", loc="center", fontsize=20)
        ax5.set_ylabel(None)
        ax5.set_xlabel(None)
        ax5.tick_params(axis='y', labelsize=15)
        ax5.tick_params(axis='x', labelsize=15)
        st.pyplot(fig)
    
    with col6:
        max_users = weather_most_users["count"].max()
        st.metric(f"Total Users in {weather_most_users['weathersit'][0]}", value=max_users)
        fig, ax6 = plt.subplots(figsize=(10,7.7))
        colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
        sns.barplot(
            y="count", 
            x="weathersit",
            data=weather_most_users,
            palette=colors,
            ax=ax6
        )
        ax6.set_title("Total Bike Rentals per Weather", loc="center", fontsize=20)
        ax6.set_ylabel(None)
        ax6.set_xlabel(None)
        ax6.tick_params(axis='y', labelsize=15)
        ax6.tick_params(axis='x', labelsize=15)
        st.pyplot(fig)

    # Visualisasi penyewaan sepeda berdasarkan kategori kecepatan angin
    max_users = windspeed_most_users["count"][0]
    st.metric(f"Total Bike Rentals in {windspeed_most_users['windspeed_category'][0]}", value=max_users)
    fig, ax = plt.subplots()
    sns.barplot(
        data=windspeed_most_users,
        x='windspeed_category',
        y='count',
        palette=["#90CAF9", "#D3D3D3", "#D3D3D3"],
        ax=ax
    )
    ax.set_title("Total bike Rentals by Windspeed Category", loc='center', fontsize=13)
    ax.set_xlabel(None)
    ax.set_ylabel(None)
    ax.tick_params(axis='y', labelsize=10)
    ax.tick_params(axis='x', labelsize=10)
    st.pyplot(fig)
    
# Tab Korelasi Fitur
with tab3:
    st.header("Relasi Suhu, Kelembaban, dan Kecepatan Angin dengan Jumlah Penyewaan Sepeda Harian")
    col1, col2, col3 = st.columns(3)

    with col1:
        temp_count_corr = round(day_df[['temp', 'count']].corr(), 2)
        st.metric(f"Korelasi temperature & count: ", value=temp_count_corr.iloc[0, 1])
        fig, ax = plt.subplots()
        sns.regplot(x="temp", y="count", data=day_df, ax=ax)
        plt.title("Relation between Temperature & Total Users", loc="center")
        plt.xlabel("Temperature (in Celcius)")
        plt.ylabel("Total Users")
        st.pyplot(fig)
        
    with col2:
        hum_count_corr = round(day_df[['humidity', 'count']].corr(), 2)
        st.metric(f"Korelasi humidity & count: ", value=hum_count_corr.iloc[0, 1])
        fig, ax = plt.subplots()
        sns.regplot(x="humidity", y="count", data=day_df, ax=ax)
        plt.title("Relation between Humidity & Total Users", loc="center")
        plt.xlabel("Humidity (%)")
        plt.ylabel("Total Users")
        st.pyplot(fig)

    with col3:
        wind_count_corr = round(day_df[['windspeed', 'count']].corr(), 2)
        st.metric(f"Korelasi windspeed & count: ", value=wind_count_corr.iloc[0, 1])
        fig, ax = plt.subplots()
        sns.regplot(x="windspeed", y="count", data=day_df, ax=ax)
        plt.title("Relation between Windspeed & Total Users", loc="center")
        plt.xlabel("Windspeed (m/s)")
        plt.ylabel("Total Users")
        st.pyplot(fig)
