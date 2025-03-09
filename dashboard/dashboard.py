import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
sns.set(style='dark')

df = pd.read_csv('dashboard/main_data.csv')

df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])


# Dashboard Title
st.title('Dashboard Analisis Data Pesanan')

# Sidebar Filters
st.sidebar.header('Filter')
min_date = df["order_purchase_timestamp"].min()
max_date = df["order_purchase_timestamp"].max()
date_range = st.sidebar.date_input(
    label = 'Pilih Rentang Tanggal',
    min_value=min_date,
    max_value=max_date,
    value=[min_date, max_date]
    )


# Apply filters
df_filtered = df[df['order_purchase_timestamp'].between(pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1]))]

# Tabs
tab1, tab2, tab3 = st.tabs(['Pesanan', 'Analisis', 'Lokasi'])

with tab1:
    st.subheader('Tren Jumlah Pesanan per Bulan')
    with st.container():
        order_trend = df_filtered.groupby(df_filtered['order_purchase_timestamp'].dt.to_period('M')).size()
        fig, ax = plt.subplots()
        order_trend.plot(marker='o', linestyle='-', ax=ax)
        plt.xlabel('Bulan')
        st.pyplot(fig)
    
    st.subheader('Rata-rata Harga Pesanan per Bulan')
    with st.container():
        avg_price_trend = df_filtered.groupby(df_filtered['order_purchase_timestamp'].dt.to_period('M'))['price'].mean()
        fig, ax = plt.subplots()
        avg_price_trend.plot(marker='s', linestyle='--', color='green', ax=ax)
        plt.xlabel('Bulan')
        st.pyplot(fig)

with tab2:
    st.subheader('Distribusi Skor Ulasan')
    with st.expander('Lihat Grafik'):
        fig, ax = plt.subplots()
        sns.countplot(data=df_filtered, x='review_score', palette='coolwarm', ax=ax)
        plt.xlabel('Skor Ulasan')
        plt.ylabel(None)
        st.pyplot(fig)
    
    st.subheader('Distribusi Harga Produk')
    with st.expander('Lihat Histogram'):
        fig, ax = plt.subplots()
        sns.histplot(df_filtered['price'], bins=50, kde=True, ax=ax)
        plt.xlim(0, df_filtered['price'].quantile(0.99))
        plt.xlabel('Harga')
        plt.ylabel(None)
        st.pyplot(fig)
    
    st.subheader('Rata-rata Harga Produk per Kategori')
    with st.expander('Lihat Grafik'):
        avg_price = df_filtered.groupby('product_category_name')['price'].mean().sort_values(ascending=False).head(10).reset_index()
        fig, ax = plt.subplots()
        sns.barplot(y='product_category_name',x='price',data=avg_price,color='magenta')
        plt.ylabel('Kategori')
        st.pyplot(fig)
    
    st.subheader('Jumlah Produk Terjual per Kategori')
    with st.expander('Lihat Grafik'):
        product_count = df_filtered['product_category_name'].value_counts().sort_values(ascending=False).head(10).reset_index()
        fig, ax = plt.subplots()
        sns.barplot(y='product_category_name',x='count',data=product_count, color='orange')
        plt.ylabel('Kategori')
        st.pyplot(fig)

with tab3:
    st.subheader('Sebaran Lokasi Pelanggan dan Penjual')
    selected_cities = (st.multiselect('Pilih Kota', df['customer_city'].unique()))
    df_location_filtered = df_filtered[df_filtered['customer_city'].isin(selected_cities)] if selected_cities else df_filtered
    with st.container():
        fig, ax = plt.subplots()
        ax.scatter(df_location_filtered['cust_lng'], df_location_filtered['cust_lat'], alpha=0.5, label='Pelanggan', color='blue', s=10)
        ax.scatter(df_location_filtered['seller_lng'], df_location_filtered['seller_lat'], alpha=0.5, label='Penjual', color='red', s=10)
        ax.legend()
        st.pyplot(fig)
    
    st.subheader('Jumlah Pesanan Berdasarkan Kota')
    with st.container():
        city_order_count = df_filtered['customer_city'].value_counts().head(10).reset_index()
        fig, ax = plt.subplots()
        sns.barplot(y='customer_city',x='count',data=city_order_count, color='purple')
        plt.ylabel('Kota')
        st.pyplot(fig)
