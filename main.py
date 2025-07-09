import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

#file_path = r"C:\Users\TimDeGreiff\Desktop\Daten1.xlsx"
#file_path = r'/Users/alexanderdegreiff/Desktop/Daten1.xlsx'

st.set_page_config(layout="wide")
st.title("Interaktive Aktienportfolio-Analyse")

st.write("""
Laden Sie Ihre Excel-Datei hoch, um die Wertentwicklung von Top 20, mittleren und Bottom 20 Analystenportfolios zu visualisieren.
""")

file_path = st.file_uploader("Wählen Sie eine Excel-Datei aus", type=["xlsx", "xls"])

if file_path is not None:
    st.success("Datei erfolgreich hochgeladen!")

st.markdown(
    """
    ---
    **Anleitung:**
    1. Klicken Sie auf "Wählen Sie eine Excel-Datei aus".
    2. Wählen Sie Ihre Excel-Datei (.xlsx oder .xls) aus, die die Ratings und Renditen enthält.
    3. Die Charts werden automatisch generiert und angezeigt.
    """
)

# Rebalancing-Zeilen
r0 = 33
r1 = 399
r2 = 765
r3 = 1129
r4 = 1494
r5 = 1860
r6 = 2225
r7 = 2590
r8 = 2955
r9 = 3321

#rebalancing_rows = [33, 399, 765, 1129, 1494, 1860, 2225, 2590, 2955, 3321]

# === Daten laden ===
sheet1 = pd.read_excel(file_path, sheet_name=0, header=None)
sheet2 = pd.read_excel(file_path, sheet_name=1, header=None)

stock_names = sheet1.iloc[, 1:51].tolist()
st.write(f" stock_names: {stock_names} ")

stock_names = pd.Series(stock_names).astype(str).str.replace(r'\s+', ' ', regex=True).str.strip()
st.write(f" stock_names2: {stock_names} ")

# === Block 1 ===
ratings0 = pd.Series(sheet1.iloc[r0, 1:51].values, index=stock_names)
ratings0 = pd.to_numeric(ratings0, errors="coerce")
top0 = ratings0.nsmallest(20).index.tolist()
mid0 = ratings0.sort_values().iloc[15:35].index.tolist()
bot0 = ratings0.nlargest(20).index.tolist()

#st.success("Datei erfolgreich hochgeladen!")
#st.write(f" bot0: {bot0} ")

returns0 = sheet2.iloc[r0+1:r1+1, 0:51].copy()
returns0.columns = ['Date'] + stock_names.tolist()
returns0['Date'] = pd.to_datetime(returns0['Date'], errors='coerce')
returns0.set_index('Date', inplace=True)
returns0.columns = returns0.columns.astype(str).str.replace(r'\s+', ' ', regex=True).str.strip()

st.write(f" returns0[bot0]: {returns0[bot0]} ")

botval0 = (returns0[bot0] / 100 + 1).cumprod().mean(axis=1) * 100
topval0 = (returns0[top0] / 100 + 1).cumprod().mean(axis=1) * 100
midval0 = (returns0[mid0] / 100 + 1).cumprod().mean(axis=1) * 100

# === Block 2 ===
ratings1 = pd.Series(sheet1.iloc[r1, 1:51].values, index=stock_names)
ratings1 = pd.to_numeric(ratings1, errors="coerce")
top1 = ratings1.nsmallest(20).index.tolist()
mid1 = ratings1.sort_values().iloc[15:35].index.tolist()
bot1 = ratings1.nlargest(20).index.tolist()

returns1 = sheet2.iloc[r1+1:r2+1, 0:51].copy()
returns1.columns = ['Date'] + stock_names.tolist()
returns1['Date'] = pd.to_datetime(returns1['Date'], errors='coerce')
returns1.set_index('Date', inplace=True)
returns1.columns = returns1.columns.astype(str).str.replace(r'\s+', ' ', regex=True).str.strip()

botval1 = (returns1[bot1] / 100 + 1).cumprod().mean(axis=1) * botval0.iloc[-1]
topval1 = (returns1[top1] / 100 + 1).cumprod().mean(axis=1) * topval0.iloc[-1]
midval1 = (returns1[mid1] / 100 + 1).cumprod().mean(axis=1) * midval0.iloc[-1]

# === Block 3 ===
ratings2 = pd.Series(sheet1.iloc[r2, 1:51].values, index=stock_names)
ratings2 = pd.to_numeric(ratings2, errors="coerce")
top2 = ratings2.nsmallest(20).index.tolist()
mid2 = ratings2.sort_values().iloc[15:35].index.tolist()
bot2 = ratings2.nlargest(20).index.tolist()

returns2 = sheet2.iloc[r2+1:r3+1, 0:51].copy()
returns2.columns = ['Date'] + stock_names.tolist()
returns2['Date'] = pd.to_datetime(returns2['Date'], errors='coerce')
returns2.set_index('Date', inplace=True)
returns2.columns = returns2.columns.astype(str).str.replace(r'\s+', ' ', regex=True).str.strip()

botval2 = (returns2[bot2] / 100 + 1).cumprod().mean(axis=1) * botval1.iloc[-1]
topval2 = (returns2[top2] / 100 + 1).cumprod().mean(axis=1) * topval1.iloc[-1]
midval2 = (returns2[mid2] / 100 + 1).cumprod().mean(axis=1) * midval1.iloc[-1]

# === Block 4 ===
ratings3 = pd.Series(sheet1.iloc[r3, 1:51].values, index=stock_names)
ratings3 = pd.to_numeric(ratings3, errors="coerce")
top3 = ratings3.nsmallest(20).index.tolist()
mid3 = ratings3.sort_values().iloc[15:35].index.tolist()
bot3 = ratings3.nlargest(20).index.tolist()

returns3 = sheet2.iloc[r3+1:r4+1, 0:51].copy()
returns3.columns = ['Date'] + stock_names.tolist()
returns3['Date'] = pd.to_datetime(returns3['Date'], errors='coerce')
returns3.set_index('Date', inplace=True)
returns3.columns = returns3.columns.astype(str).str.replace(r'\s+', ' ', regex=True).str.strip()

botval3 = (returns3[bot3] / 100 + 1).cumprod().mean(axis=1) * botval2.iloc[-1]
topval3 = (returns3[top3] / 100 + 1).cumprod().mean(axis=1) * topval2.iloc[-1]
midval3 = (returns3[mid3] / 100 + 1).cumprod().mean(axis=1) * midval2.iloc[-1]

# === Block 5 ===
ratings4 = pd.Series(sheet1.iloc[r4, 1:51].values, index=stock_names)
ratings4 = pd.to_numeric(ratings4, errors="coerce")
top4 = ratings4.nsmallest(20).index.tolist()
mid4 = ratings4.sort_values().iloc[15:35].index.tolist()
bot4 = ratings4.nlargest(20).index.tolist()

returns4 = sheet2.iloc[r4+1:r5+1, 0:51].copy()
returns4.columns = ['Date'] + stock_names.tolist()
returns4['Date'] = pd.to_datetime(returns4['Date'], errors='coerce')
returns4.set_index('Date', inplace=True)
returns4.columns = returns4.columns.astype(str).str.replace(r'\s+', ' ', regex=True).str.strip()

botval4 = (returns4[bot4] / 100 + 1).cumprod().mean(axis=1) * botval3.iloc[-1]
topval4 = (returns4[top4] / 100 + 1).cumprod().mean(axis=1) * topval3.iloc[-1]
midval4 = (returns4[mid4] / 100 + 1).cumprod().mean(axis=1) * midval3.iloc[-1]

# === Block 6 ===
ratings5 = pd.Series(sheet1.iloc[r5, 1:51].values, index=stock_names)
ratings5 = pd.to_numeric(ratings5, errors="coerce")
top5 = ratings5.nsmallest(20).index.tolist()
mid5 = ratings5.sort_values().iloc[15:35].index.tolist()
bot5 = ratings5.nlargest(20).index.tolist()

returns5 = sheet2.iloc[r5+1:r6+1, 0:51].copy()
returns5.columns = ['Date'] + stock_names.tolist()
returns5['Date'] = pd.to_datetime(returns5['Date'], errors='coerce')
returns5.set_index('Date', inplace=True)
returns5.columns = returns5.columns.astype(str).str.replace(r'\s+', ' ', regex=True).str.strip()

botval5 = (returns5[bot5] / 100 + 1).cumprod().mean(axis=1) * botval4.iloc[-1]
topval5 = (returns5[top5] / 100 + 1).cumprod().mean(axis=1) * topval4.iloc[-1]
midval5 = (returns5[mid5] / 100 + 1).cumprod().mean(axis=1) * midval4.iloc[-1]


# === Block 7 ===
ratings6 = pd.Series(sheet1.iloc[r6, 1:51].values, index=stock_names)
ratings6 = pd.to_numeric(ratings6, errors="coerce")
top6 = ratings6.nsmallest(20).index.tolist()
mid6 = ratings6.sort_values().iloc[15:35].index.tolist()
bot6 = ratings6.nlargest(20).index.tolist()

returns6 = sheet2.iloc[r6+1:r7+1, 0:51].copy()
returns6.columns = ['Date'] + stock_names.tolist()
returns6['Date'] = pd.to_datetime(returns6['Date'], errors='coerce')
returns6.set_index('Date', inplace=True)
returns6.columns = returns6.columns.astype(str).str.replace(r'\s+', ' ', regex=True).str.strip()

botval6 = (returns6[bot6] / 100 + 1).cumprod().mean(axis=1) * botval5.iloc[-1]
topval6 = (returns6[top6] / 100 + 1).cumprod().mean(axis=1) * topval5.iloc[-1]
midval6 = (returns6[mid6] / 100 + 1).cumprod().mean(axis=1) * midval5.iloc[-1]


# === Block 8 ===
ratings7 = pd.Series(sheet1.iloc[r7, 1:51].values, index=stock_names)
ratings7 = pd.to_numeric(ratings7, errors="coerce")
top7 = ratings7.nsmallest(20).index.tolist()
mid7 = ratings7.sort_values().iloc[15:35].index.tolist()
bot7 = ratings7.nlargest(20).index.tolist()

returns7 = sheet2.iloc[r7+1:r8+1, 0:51].copy()
returns7.columns = ['Date'] + stock_names.tolist()
returns7['Date'] = pd.to_datetime(returns7['Date'], errors='coerce')
returns7.set_index('Date', inplace=True)
returns7.columns = returns7.columns.astype(str).str.replace(r'\s+', ' ', regex=True).str.strip()

botval7 = (returns7[bot7] / 100 + 1).cumprod().mean(axis=1) * botval6.iloc[-1]
topval7 = (returns7[top7] / 100 + 1).cumprod().mean(axis=1) * topval6.iloc[-1]
midval7 = (returns7[mid7] / 100 + 1).cumprod().mean(axis=1) * midval6.iloc[-1]

# === Block 9 ===
ratings8 = pd.Series(sheet1.iloc[r8, 1:51].values, index=stock_names)
ratings8 = pd.to_numeric(ratings8, errors="coerce")
top8 = ratings8.nsmallest(20).index.tolist()
mid8 = ratings8.sort_values().iloc[15:35].index.tolist()
bot8 = ratings8.nlargest(20).index.tolist()

returns8 = sheet2.iloc[r8+1:r9+1, 0:51].copy()
returns8.columns = ['Date'] + stock_names.tolist()
returns8['Date'] = pd.to_datetime(returns8['Date'], errors='coerce')
returns8.set_index('Date', inplace=True)
returns8.columns = returns8.columns.astype(str).str.replace(r'\s+', ' ', regex=True).str.strip()

botval8 = (returns8[bot8] / 100 + 1).cumprod().mean(axis=1) * botval7.iloc[-1]
topval8 = (returns8[top8] / 100 + 1).cumprod().mean(axis=1) * topval7.iloc[-1]
midval8 = (returns8[mid8] / 100 + 1).cumprod().mean(axis=1) * midval7.iloc[-1]

# === Block 9 ===
ratings9 = pd.Series(sheet1.iloc[r9, 1:51].values, index=stock_names)
ratings9 = pd.to_numeric(ratings9, errors="coerce")
top9 = ratings9.nsmallest(20).index.tolist()
mid9 = ratings9.sort_values().iloc[15:35].index.tolist()
bot9 = ratings9.nlargest(20).index.tolist()

returns9 = sheet2.iloc[r9+1:, 0:51].copy()
returns9.columns = ['Date'] + stock_names.tolist()
returns9['Date'] = pd.to_datetime(returns9['Date'], errors='coerce')
returns9.set_index('Date', inplace=True)
returns9.columns = returns9.columns.astype(str).str.replace(r'\s+', ' ', regex=True).str.strip()

botval9 = (returns9[bot9] / 100 + 1).cumprod().mean(axis=1) * botval8.iloc[-1]
topval9 = (returns9[top9] / 100 + 1).cumprod().mean(axis=1) * topval8.iloc[-1]
midval9 = (returns9[mid9] / 100 + 1).cumprod().mean(axis=1) * midval8.iloc[-1]

# === Zusammenfügen der Werte (bis Block 4 als Beispiel) ===
top_all = pd.concat([topval0, topval1, topval2, topval3, topval4, topval5, topval6, topval7, topval8, topval9])
mid_all = pd.concat([midval0, midval1, midval2, midval3, midval4, midval5, midval6, midval7, midval8, midval9])
bot_all = pd.concat([botval0, botval1, botval2, botval3, botval4, botval5, botval6, botval7, botval8, botval9])


# === Plot ===
plt.figure(figsize=(12, 6))
plt.plot(top_all.index, top_all, label="Top 20 Portfolio", color="green")
plt.plot(mid_all.index, mid_all, label="Benchmark (Mitte 20)", color="blue")
plt.plot(bot_all.index, bot_all, label="Bottom 20 Portfolio", color="red")
plt.title("Top vs Mitte vs Bottom Analystenportfolios (2016–2025)")
plt.xlabel("Datum")
plt.ylabel("Portfoliowert (Start = 100)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
