import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from pathlib import Path

sns.set(style='darkgrid')

st.subheader("Data")
def PengaruhHariKerja_df(df):
    PengaruhHariKerja = df.groupby(by="workingday").instant.nunique().reset_index()
    PengaruhHariKerja.rename(columns={"instant": "sum"}, inplace=True)
    PengaruhHariKerja

    return PengaruhHariKerja


def PengaruhCuaca_df(df):
    PengaruhCuaca = df.groupby(by="weathersit").instant.nunique().reset_index()
    PengaruhCuaca.rename(columns={"instant": "sum"}, inplace=True)
    PengaruhCuaca

    return PengaruhCuaca


def sidebar(df):
    df["tanggal"] = pd.to_datetime(df["tanggal"])
    min_date = df["tanggal"].min()
    max_date = df["tanggal"].max()

    with st.sidebar:
        st.image("D:\A SEMESTER 6 CODING CAMP DBS\Belajar Dasar Analisis Data Dengan Python\ProyekAkhir_BelajarAnalisisDataPython-main\dashboard\images.jpg", width=250)

        st.markdown("<h2 style='text-align: center; color: #FF5733;'>🚴 Bike Sharing Dashboard</h2>", unsafe_allow_html=True)
        
        st.markdown(
            "<p style='text-align: center;'>Selamat datang! Gunakan filter di bawah ini untuk melihat data peminjaman sepeda berdasarkan rentang tanggal yang diinginkan.</p>",
            unsafe_allow_html=True
        )

        def on_change():
            st.session_state.date = date

        date = st.date_input(
            label="📅 Pilih Rentang Waktu",
            min_value=min_date,
            max_value=max_date,
            value=[min_date, max_date],
            on_change=on_change
        )

        st.markdown("---")
        st.info("🔹 Data mencakup seluruh peminjaman sepeda dalam rentang waktu yang tersedia.")

    return date

# load dataset
day_bike = pd.read_csv("dashboard.csv")

date = sidebar(day_df)
if len(date) == 2:
    main_df = day_df[(day_df["tanggal"] >= str(date[0])) & (day_df["tanggal"] <= str(date[1]))]
else:
    main_df = day_df[
        (day_df["tanggal"] >= str(st.session_state.date[0])) & (day_df["tanggal"] <= str(st.session_state.date[1]))]

PengaruhHariKerja = PengaruhHariKerja_df(main_df)
PengaruhCuaca = PengaruhCuaca_df(main_df)

st.header("Bike Sharing Dashboard 🚴")
st.markdown("### Analisis Pengaruh Faktor Eksternal terhadap Jumlah Pengguna Bike Sharing")

st.subheader("Pengaruh Hari Kerja terhadap Jumlah Pengguna")
fig, ax = plt.subplots(figsize=(6, 4))
sns.barplot(x="workingday", y="sum", data=PengaruhHariKerja, palette="coolwarm", ax=ax)
ax.set_xlabel("Hari Kerja (0 = Tidak, 1 = Ya)")
ax.set_ylabel("Jumlah Pengguna")
ax.set_title("Pengaruh Hari Kerja terhadap Jumlah Pengguna")
st.pyplot(fig)

st.subheader("Pengaruh Cuaca terhadap Jumlah Pengguna")
fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x="weathersit", y="sum", hue="weathersit", data=PengaruhCuaca, palette="coolwarm", legend=False, ax=ax)
ax.set_xlabel("Kondisi Cuaca")
ax.set_ylabel("Jumlah Pengguna")
ax.set_title("Pengaruh Cuaca terhadap Jumlah Pengguna")
ax.set_xticks([0, 1, 2, 3])
ax.set_xticklabels(["Cerah", "Berawan", "Hujan", "Salju"], rotation=30)
st.pyplot(fig)

st.subheader("Pengaruh Temperatur terhadap Pengguna Bike Sharing")
fig, ax = plt.subplots(figsize=(8, 5))
sns.scatterplot(x=day_df["temp"], y=day_df["cnt"], alpha=0.6, color="blue", ax=ax)
ax.set_xlabel("Temperatur Normal dalam Celcius")
ax.set_ylabel("Jumlah Pengguna")
ax.set_title("Scatter Plot Pengaruh Temperatur terhadap Pengguna Bike Sharing")
st.pyplot(fig)

if __name__ == "__main__":
    st.caption("Copyright © 2025 | Bike Sharing Dashboard | All Rights Reserved | Made by: [@annisapeb_9]")
