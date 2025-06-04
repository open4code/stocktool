# pip install streamlit yfinance pandas

# 
#
#

import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import date # Für Datumsauswahl

st.title("Aktienanalyse-Tool")

# Sidebar für Eingaben
st.sidebar.header("Einstellungen")

ticker_symbol = st.sidebar.text_input("Aktiensymbol (Ticker), z.B. AAPL", "AAPL") # Standardwert: AAPL

# Datumsauswahl für historische Daten
today = date.today()
start_date = st.sidebar.date_input("Startdatum", value=pd.to_datetime("2023-01-01")) # Ein vernünftiges Startdatum
end_date = st.sidebar.date_input("Enddatum", value=today)

# Daten für den Ticker laden
ticker_data = yf.Ticker(ticker_symbol)

# Aktuelle Informationen und Fundamentaldaten
# yfinance speichert viele Infos im .info Attribut als Dictionary
try:
    stock_info = ticker_data.info
    if not stock_info: # Check if info is empty (e.g., invalid ticker)
         st.error(f"Fehler: Konnte keine Daten für Ticker '{ticker_symbol}' abrufen. Vielleicht ist der Ticker ungültig?")
    else:

        # zum debugggen mal eine tabelle mit allen infos drucken
        st.dataframe(stock_info)
        
        # Grundlegende Informationen anzeigen
        st.subheader(f"Informationen zu {stock_info.get('shortName', ticker_symbol)}") # Zeige Kurznamen, falls verfügbar

        # Börsenkurs (Letzter Schluss- oder aktueller Preis)
        # yfinance info hat oft den letzten Schlusskurs in regularMarketPreviousClose oder den aktuellen in regularMarketPrice
        current_price = stock_info.get('regularMarketPrice')
        if current_price:
            st.write(f"Aktueller/Letzter Kurs: **{current_price:.2f}** {stock_info.get('currency', '')}")

        # KGV (Kurs-Gewinn-Verhältnis)
        # yfinance info hat oft trailingPE (für die letzten 12 Monate) oder forwardPE (geschätzt für die Zukunft)
        trailing_pe = stock_info.get('trailingPE')
        if trailing_pe is not None: # None prüfen, da 0 ein gültiges KGV ist, aber fehlend nicht
            st.write(f"KGV (TTM): **{trailing_pe:.2f}**")
        else:
            st.write("KGV (TTM): Daten nicht verfügbar")

        # Weitere nützliche Daten aus .info anzeigen, falls vorhanden (später mehr dazu)
        market_cap = stock_info.get('marketCap')
        if market_cap:
            st.write(f"Marktkapitalisierung: {market_cap:,} {stock_info.get('currency', '')}") # Format mit Tausendertrennzeichen

except Exception as e:
    st.error(f"Ein Fehler ist aufgetreten beim Abrufen der Finanzinformationen: {e}")
    st.write("Bitte überprüfen Sie den Ticker und Ihre Internetverbindung.")

# Historische Daten
try:
    hist_data = ticker_data.history(start=start_date, end=end_date)

    if hist_data.empty:
        st.warning("Keine historischen Daten für den ausgewählten Zeitraum verfügbar.")
    else:
        st.subheader("Historischer Kursverlauf")

        # Anzeige der Tabelle mit historischen Daten
        # st.dataframe(hist_data) # Optional: Historische Daten als Tabelle anzeigen

        # Anzeige des Kursverlaufs als Liniendiagramm
        # Wir zeigen standardmäßig den Schlusskurs ('Close')
        st.line_chart(hist_data['Close'])

        # Optional: Chart kann auch andere Spalten enthalten, z.B. Volume
        # st.line_chart(hist_data[['Close', 'Volume']])


except Exception as e:
    st.error(f"Ein Fehler ist aufgetreten beim Abrufen der historischen Daten: {e}")
    st.write("Bitte überprüfen Sie den Ticker und den Datumsbereich.")
