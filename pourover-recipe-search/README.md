# 🏆 Championship Coffee Recipe Finder

A tiny Streamlit app that searches the web (via Exa) for championship-level coffee recipes, with optional required-text filtering.

## Local Setup

```bash
git clone https://github.com/<your-username>/exa-coffee-app.git
cd exa-coffee-app
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
export EXA_API_KEY="YOUR_EXA_API_KEY"
streamlit run app.py
