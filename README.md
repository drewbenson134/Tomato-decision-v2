# HORT 2000 Tomato Decision Lab — Version 2

Upload `app.py` and `requirements.txt` to a GitHub repository, then deploy on Streamlit Community Cloud with entrypoint `app.py`.

To run locally:

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

## Student workflow
1. Read invented scouting evidence; lock initial prediction and rationale.
2. Compare three strategies with editable economic assumptions.
3. Consult the four original Gemini Gems; document their concerns and responses.
4. Reveal a seven-day update and interpret field-margin vs interior counts.
5. Defend and revise decision, including biology, economics, stakeholder concerns, label and harvest feasibility.
6. Self-review and download a CSV of responses and numerical assumptions.

### Important limitations
- Invented whitefly counts are **not** treatment thresholds. Symptoms are not virus confirmations.
- Model estimates are conditional arithmetic, not actual field forecasts or treatment efficacy benchmarks.
- The four Gemini Gems are external websites, with their own account/sharing requirements. The app does not access Gemini conversation data.
- Streamlit session state lasts for a browser session; students should export CSV before leaving.
- Browser testing was not possible in this environment; Python syntax and the core model have been checked.

References:
- https://fieldreport.caes.uga.edu/publications/B1312/commercial-tomato-production-handbook/
- https://ipm.uga.edu/georgia-pest-management-handbook/
- https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app
