
# Minervini Stock Analyzer - Streamlit App
# All code, requirements, and setup for GitHub and Streamlit deployment

import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import datetime
from fpdf import FPDF

# Helper Functions
def fetch_stock_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1y")
        info = stock.info
        return hist, info
    except Exception as e:
        return None, None

def calculate_eps_growth(info):
    try:
        return info['earningsQuarterlyGrowth']
    except:
        return None

def calculate_peg_ratio(info):
    try:
        return info['pegRatio']
    except:
        return None

def analyze_promoter_dii(ticker):
    # Mocking placeholder: replace with screener.in scraping or API
    return {
        'promoter_change': "+0.6%",
        'dii_change': "-0.4%"
    }

def calculate_rs_rating(hist):
    try:
        perf = (hist['Close'].iloc[-1] - hist['Close'].iloc[0]) / hist['Close'].iloc[0] * 100
        return min(100, max(0, int(perf)))
    except:
        return None

def generate_pdf_report(ticker, analysis):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Stock Analysis Report: {ticker}", ln=1, align='C')
    pdf.ln(10)

    for key, value in analysis.items():
        pdf.cell(200, 10, txt=f"{key}: {value}", ln=1)

    pdf.output("analysis_report.pdf")

# Streamlit UI
st.title("Minervini Stock Analyzer (India)")
ticker = st.text_input("Enter NSE Stock Ticker (e.g., TCS.NS):")

if ticker:
    hist, info = fetch_stock_data(ticker)

    if hist is not None and info is not None:
        eps_growth = calculate_eps_growth(info)
        peg = calculate_peg_ratio(info)
        holdings = analyze_promoter_dii(ticker)
        rs = calculate_rs_rating(hist)

        summary = {
            'EPS Growth (QoQ)': f"{eps_growth:.2%}" if eps_growth else "N/A",
            'PEG Ratio': peg if peg else "N/A",
            'Promoter Holding Change': holdings['promoter_change'],
            'DII Holding Change': holdings['dii_change'],
            'RS Rating': rs
        }

        decision = "YES" if eps_growth and eps_growth > 0.25 and peg < 1.5 else "PARTIAL / NO"

        st.subheader("Analysis Summary")
        for k, v in summary.items():
            st.write(f"**{k}:** {v}")

        st.markdown(f"### Final Verdict: **{decision}**")

        if st.button("Generate PDF Report"):
            generate_pdf_report(ticker, summary)
            with open("analysis_report.pdf", "rb") as f:
                st.download_button("Download PDF", f, file_name="analysis_report.pdf")

        st.line_chart(hist['Close'])
    else:
        st.error("Could not fetch stock data. Check ticker.")
