import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def process_excel_data(file_path):
    """
    Diese Funktion verarbeitet die Excel-Daten und generiert die Portfoliowerte.
    """
    # Rebalancing-Zeilen
    rebalancing_rows = [33, 399, 765, 1129, 1494, 1860, 2225, 2590, 2955, 3321]

    # === Daten laden ===
    sheet1 = pd.read_excel(file_path, sheet_name=0, header=None)
    sheet2 = pd.read_excel(file_path, sheet_name=1, header=None)

    stock_names = sheet1.iloc[0, 1:51].tolist()
    stock_names = pd.Series(stock_names).astype(str).str.replace(r'\s+', ' ', regex=True).str.strip()

    all_top_vals = []
    all_mid_vals = []
    all_bot_vals = []

    previous_top_val_last = 100
    previous_mid_val_last = 100
    previous_bot_val_last = 100

    for i in range(len(rebalancing_rows)):
        r_start = rebalancing_rows[i]
        if i < len(rebalancing_rows) - 1:
            r_end = rebalancing_rows[i+1]
        else:
            r_end = None # Bis zum Ende der Tabelle

        # Ratings
        ratings = pd.Series(sheet1.iloc[r_start, 1:51].values, index=stock_names)
        ratings = pd.to_numeric(ratings, errors="coerce")
        top_stocks = ratings.nsmallest(20).index.tolist()
        mid_stocks = ratings.sort_values().iloc[15:35].index.tolist()
        bot_stocks = ratings.nlargest(20).index.tolist()

        # Returns
        if r_end is not None:
            returns = sheet2.iloc[r_start+1:r_end+1, 0:51].copy()
        else:
            returns = sheet2.iloc[r_start+1:, 0:51].copy()

        returns.columns = ['Date'] + stock_names.tolist()
        returns['Date'] = pd.to_datetime(returns['Date'], errors='coerce')
        returns.set_index('Date', inplace=True)
        returns.columns = returns.columns.astype(str).str.replace(r'\s+', ' ', regex=True).str.strip()

        # Portfoliowerte berechnen
        selected_bot_returns = returns[bot_stocks]
        selected_top_returns = returns[top_stocks]
        selected_mid_returns = returns[mid_stocks]

        # Optional: Debugging-Ausgabe, um Spalten und Daten zu überprüfen
        st.write(f"Ausgewählte Bot-Spalten: {selected_bot_returns.columns.tolist()}")
        st.write(f"Beispiel Bot-Renditen:\n{selected_bot_returns.head()}")

        # Konvertieren Sie die ausgewählten Daten explizit zu numerischen Werten (falls nicht bereits geschehen)
        # Dies ist eine wichtige Fehlerquelle: Sicherstellen, dass es sich um Zahlen handelt
        selected_bot_returns = selected_bot_returns.apply(pd.to_numeric, errors='coerce')
        selected_top_returns = selected_top_returns.apply(pd.to_numeric, errors='coerce')
        selected_mid_returns = selected_mid_returns.apply(pd.to_numeric, errors='coerce')

        # Füllen Sie NaN-Werte, wenn nötig, um Fehler bei Berechnungen zu vermeiden.
        # Eine Option wäre 0 oder der Mittelwert/Median, je nach Datenlage.
        # Für Renditen ist 0 oft eine sichere Wahl, damit cumprod nicht unterbrochen wird.
        selected_bot_returns = selected_bot_returns.fillna(0)
        selected_top_returns = selected_top_returns.fillna(0)
        selected_mid_returns = selected_mid_returns.fillna(0)

        botval = (selected_bot_returns / 100 + 1).cumprod().mean(axis=1) * previous_bot_val_last
        topval = (selected_top_returns / 100 + 1).cumprod().mean(axis=1) * previous_top_val_last
        midval = (selected_mid_returns / 100 + 1).cumprod().mean(axis=1) * previous_mid_val_last

        all_top_vals.append(topval)
        all_mid_vals.append(midval)
        all_bot_vals.append(botval)

        previous_top_val_last = topval.iloc[-1] if not topval.empty else previous_top_val_last
        previous_mid_val_last = midval.iloc[-1] if not midval.empty else previous_mid_val_last
        previous_bot_val_last = botval.iloc[-1] if not botval.empty else previous_bot_val_last

    top_all = pd.concat(all_top_vals)
    mid_all = pd.concat(all_mid_vals)
    bot_all = pd.concat(all_bot_vals)

    return top_all, mid_all, bot_all

st.set_page_config(layout="wide")
st.title("Interaktive Aktienportfolio-Analyse")

st.write("""
Laden Sie Ihre Excel-Datei hoch, um die Wertentwicklung von Top 20, mittleren und Bottom 20 Analystenportfolios zu visualisieren.
""")

uploaded_file = st.file_uploader("Wählen Sie eine Excel-Datei aus", type=["xlsx", "xls"])

if uploaded_file is not None:
    st.success("Datei erfolgreich hochgeladen!")
    try:
        # Verarbeiten der Daten
        top_all, mid_all, bot_all = process_excel_data(uploaded_file)

        # === Plot ===
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(top_all.index, top_all, label="Top 20 Portfolio", color="green")
        ax.plot(mid_all.index, mid_all, label="Benchmark (Mitte 20)", color="blue")
        ax.plot(bot_all.index, bot_all, label="Bottom 20 Portfolio", color="red")
        ax.set_title("Top vs Mitte vs Bottom Analystenportfolios (2016–2025)")
        ax.set_xlabel("Datum")
        ax.set_ylabel("Portfoliowert (Start = 100)")
        ax.legend()
        ax.grid(True)
        plt.tight_layout()

        st.pyplot(fig)

    except Exception as e:
        st.error(f"Fehler bei der Verarbeitung der Datei: {e}")
        st.info("Bitte stellen Sie sicher, dass Ihre Excel-Datei das erwartete Format hat (zwei Sheets mit den entsprechenden Daten).")

st.markdown(
    """
    ---
    **Anleitung:**
    1. Klicken Sie auf "Wählen Sie eine Excel-Datei aus".
    2. Wählen Sie Ihre Excel-Datei (.xlsx oder .xls) aus, die die Ratings und Renditen enthält.
    3. Die Charts werden automatisch generiert und angezeigt.
    """
)
