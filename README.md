# NSE Pro Swing Scanner (2025-2026 Edition) 🚀

**A professional-grade, high-probability swing trading system for the Indian stock market.**

This is not just a "scanner" — it is a **capital preservation system**. It filters out 99% of noise to find the top 1% of "Sniper" setups with 5-10% weekly upside potential.

---

## � Key Features

### 1. The "Sniper" Scanner (`weekly_swing_scanner.py`)
- **Universe**: Scans top **1000 liquid NSE stocks**.
- **Philosophy**: "Cash is a position." If no A+ setups exist, it returns 0 results.
- **9 High-Probability Filters**:
  1.  **52-Week High**: Must be within 25% of 52-week high.
  2.  **Trend**: Price > 2% above 200-day SMA.
  3.  **VCP (Volatility Contraction)**: 10-day range must be ≤ 12%.
  4.  **RSI Cap**: RSI must be < 70 (no overbought chasing).
  5.  **Momentum Cap**: < 18% up in last 2 weeks (no FOMO).
  6.  **Volume**: Today's volume > 80% of 10-day average.
  7.  **Risk Control**: Max risk per trade capped at 7%.
  8.  **Risk:Reward**: Minimum 1:1.3 for the first 5% target.
  9.  **Relative Strength**: Must outperform Nifty by 10%+ over the last month.

### 2. Interactive Dashboard (`app.py`)
- Built with **Streamlit**.
- View scan results in a beautiful, sortable table.
- Filter by Price, RSI, Risk %, and Momentum.
- Download filtered results to CSV.

### 3. Fully Automated (`GitHub Actions`)
- Runs **automatically every day at 3:30 PM IST** (Market Close).
- Auto-commits results to the repo.
- You just check the dashboard!

---

## 🛠️ Installation & Usage

### Prerequisites
- Python 3.9+
- Git

### 1. Clone & Install
```bash
git clone https://github.com/YourUsername/Weekly_SwingTrades_Scanner.git
cd Weekly_SwingTrades_Scanner
pip install -r requirements.txt
```

### 2. Run the Scanner Manually
```bash
python weekly_swing_scanner.py
```
*Output: `SWING_PRO_YYYYMMDD_HHMM.csv` and `.xlsx`*

### 3. Launch the Dashboard
```bash
streamlit run app.py
```
*Opens in your browser at `http://localhost:8501`*

---

## 📊 Output Format

| Column | Description |
|--------|-------------|
| **Symbol** | NSE Symbol (e.g., RELIANCE) |
| **Buy_Range** | Precise entry zone (±1%) |
| **Target_5pct** | First profit target (+5%) |
| **Target_10pct** | Runner target (+10%) |
| **Stop_Loss** | Hard stop (below consolidation) |
| **Risk_Reward** | R:R ratio (e.g., 1:2.5) |
| **RS_vs_Nifty** | Outperformance vs Benchmark |
| **Risk%** | Capital at risk (max 7%) |

---

## 🤖 Automation (GitHub Actions)

The scanner is configured to run automatically via **GitHub Actions**.
- **Schedule**: Every day at **3:30 PM IST**.
- **Workflow File**: `.github/workflows/daily_scanner.yml`
- **Artifacts**: Results are uploaded as build artifacts and committed to the repo.

---

## ⚠️ Trading Rules (The "Edge")

1.  **Zero Signals is Good**: If the scanner finds nothing, the market is likely overextended or choppy. **Stay in cash.**
2.  **Entry**: Buy only within the `Buy_Range`. Do not chase gap-ups.
3.  **Risk Management**: Never risk more than 1-2% of your total capital on a single trade.
4.  **Exit**: Sell 50% at `Target_5pct`, move SL to breakeven, and ride the rest to `Target_10pct`.

---

**Disclaimer**: This tool is for educational purposes only. I am not a SEBI registered advisor. Trading stocks involves risk.