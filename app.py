"""HORT 2000 Tomato Decision Lab V2 — hypothetical educational simulation."""
import csv
import io
from datetime import datetime

import pandas as pd
import streamlit as st

st.set_page_config(page_title="HORT 2000 | Tomato Decision Lab V2", page_icon="🍅", layout="wide")

GEMS = {
    "Alex Morgan — Vegetable Grower": (
        "https://gemini.google.com/gem/10Ru1BVom8p37xHWD502GtTkUXFPd9plC?usp=sharing",
        "Profitability, labor, production risk and feasibility",
        "What costs and risks would make you reject my proposal?",
    ),
    "Casey Brooks — Produce Buyer": (
        "https://gemini.google.com/gem/1eSuOvG5v-p1zQf_rcp7MbkAZwWvLx5mu?usp=sharing",
        "Product quality, delivery schedules and buyer requirements",
        "Which market requirements might my plan jeopardize?",
    ),
    "Jordan Ellis — Environmental Advocate": (
        "https://gemini.google.com/gem/1HqIw7ygpAdf5UZQJ1ec2EzvPbGoW_9ZH?usp=sharing",
        "Beneficial insects, nontarget exposure and resistance",
        "Which environmental tradeoff is hardest to justify?",
    ),
    "Dr. Taylor Reed — Extension Specialist": (
        "https://gemini.google.com/gem/1nvwxKxreYLeIsfeB1eoQXO4JkE8rnIYd?usp=sharing",
        "Pest identification, monitoring and evidence-based IPM",
        "What scouting evidence is still missing before treatment?",
    ),
}
STRATEGIES = [
    "Intensified scouting + targeted intervention",
    "Immediate broad-area application",
    "Scouting + primarily nonchemical measures",
]
# Demonstration-only cost and effectiveness assumptions, NOT UGA recommendations.
DEFAULT_COSTS = [4000, 6500, 2500]
DEFAULT_AVOIDED = [50, 70, 25]
BASE_SCOUTING = pd.DataFrame({
    "Week": ["Week 1", "Week 2"],
    "Adults / sampled leaf": [2.1, 6.4],
    "Nymphs / sampled leaf": [3.5, 8.8],
    "Plants with TYLCV-like symptoms (%)": [1.0, 3.0],
    "Sampled plants with natural enemies (%)": [35.0, 25.0],
})
UPDATE_DATA = pd.DataFrame({
    "Field zone": ["Field margin", "Interior"],
    "Adult whiteflies / sampled leaf": [13.1, 5.2],
    "Nymphs / sampled leaf": [16.0, 7.0],
})


def money(value):
    return f"${value:,.0f}"


def calculate(gross, loss_pct, cost, avoided_pct):
    """Simple assumed incremental benefit; not total profit or a pest forecast."""
    threatened = gross * loss_pct / 100
    preserved = threatened * avoided_pct / 100
    return threatened, preserved, preserved - cost


def init_state():
    defaults = {
        "locked": False,
        "initial_strategy_locked": "",
        "initial_reason_locked": "",
        "initial_evidence_locked": "",
        "update_revealed": False,
        "reviewed": False,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def export_csv():
    state = st.session_state
    records = [
        ("Initial strategy", state.get("initial_strategy_locked", "")),
        ("Initial reasoning", state.get("initial_reason_locked", "")),
        ("Initial scouting interpretation", state.get("initial_evidence_locked", "")),
        ("Seven-day evidence revealed", str(state.get("update_revealed", False))),
        ("Seven-day interpretation", state.get("update_interpretation", "")),
        ("Final strategy", state.get("final_strategy", "")),
        ("Final biological justification", state.get("final_biology", "")),
        ("Final economic justification", state.get("final_economics", "")),
        ("Change in reasoning", state.get("reasoning_change", "")),
        ("Unresolved uncertainty", state.get("final_uncertainty", "")),
        ("Management feasibility", state.get("feasibility", "")),
        ("Acreage", state.get("acres", 10)),
        ("Yield lb/acre", state.get("yield_lb", 30000)),
        ("Price dollars/lb", state.get("price", 0.80)),
        ("Untreated loss % (assumption)", state.get("loss_pct", 20)),
        ("Budget dollars", state.get("budget", 8000)),
    ]
    for i, strategy in enumerate(STRATEGIES):
        records.extend([
            (f"{strategy}: cost dollars", state.get(f"cost_{i}", DEFAULT_COSTS[i])),
            (f"{strategy}: losses avoided % (assumption)", state.get(f"avoided_{i}", DEFAULT_AVOIDED[i])),
        ])
    for name in GEMS:
        records.extend([
            (f"{name}: concern", state.get(f"concern_{name}", "")),
            (f"{name}: response", state.get(f"response_{name}", "")),
        ])
    for key in ("rubric_biology", "rubric_economics", "rubric_stakeholders", "rubric_revision"):
        records.append((key, str(state.get(key, False))))
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Field", "Response"])
    writer.writerows(records)
    return output.getvalue()


init_state()
st.title("🍅 The Georgia Tomato Dilemma")
st.caption("HORT 2000 • Evidence → Prediction → Economics → Stakeholders → New evidence → Revision")
st.warning(
    "All scouting counts, prices, efficacy estimates, and events are invented for teaching. "
    "This is not an economic threshold, validated pest forecast, pesticide recommendation, or product label. "
    "Consult current UGA Extension guidance and applicable labels for real decisions."
)

tabs = st.tabs([
    "1 · Evidence & prediction", "2 · Economic choices", "3 · Stakeholder Gems",
    "4 · Seven-day update", "5 · Final decision", "6 · Review & export",
])

with tabs[0]:
    st.subheader("Case: fall fresh-market tomatoes in South Georgia")
    st.write(
        "Alex Morgan grows 10 acres of fresh-market fall tomatoes on plastic-mulched beds with drip irrigation. "
        "Harvest begins in approximately 21 days. Sweetpotato whiteflies have been observed, "
        "and some plants show symptoms consistent with tomato yellow leaf curl virus (TYLCV), "
        "but viral infection has **not** been laboratory-confirmed. An earlier whitefly-directed "
        "treatment was applied; its product, mode of action, and effectiveness must be verified. "
        "The buyer expects a reliable, compliant shipment."
    )
    st.markdown("#### Simulated scouting report")
    st.dataframe(BASE_SCOUTING, use_container_width=True, hide_index=True)
    st.line_chart(BASE_SCOUTING.set_index("Week")[["Adults / sampled leaf", "Nymphs / sampled leaf"]])
    st.caption(
        "Counts are hypothetical means using an assumed consistent leaf-selection protocol; "
        "they are NOT validated action thresholds. Symptom frequency does not confirm TYLCV. "
        "No treatment should be chosen solely from these numbers."
    )
    st.info(
        "Before deciding, consider scouting design, pest identification, virus confirmation, "
        "field distribution, beneficial insects, prior treatments, and harvest restrictions."
    )
    if st.session_state.locked:
        st.success("Initial decision locked. Continue to economics and stakeholder consultations.")
        st.write("**Initial strategy:**", st.session_state.initial_strategy_locked)
        st.write("**Initial rationale:**", st.session_state.initial_reason_locked)
        st.write("**Scouting interpretation:**", st.session_state.initial_evidence_locked)
    else:
        st.selectbox("Initial management strategy", STRATEGIES, key="initial_strategy")
        st.text_area("What do the scouting observations suggest, and what remains unknown?", key="initial_evidence", height=110)
        st.text_area("Why is this your initial choice? Defend it using crop biology and uncertainty.", key="initial_reason", height=110)
        if st.button("Lock in my initial decision", type="primary"):
            if not st.session_state.initial_evidence.strip() or not st.session_state.initial_reason.strip():
                st.error("Complete both written explanations before locking your prediction.")
            else:
                st.session_state.initial_strategy_locked = st.session_state.initial_strategy
                st.session_state.initial_reason_locked = st.session_state.initial_reason.strip()
                st.session_state.initial_evidence_locked = st.session_state.initial_evidence.strip()
                st.session_state.locked = True
                st.rerun()

with tabs[1]:
    st.subheader("Compare three management alternatives")
    st.write(
        "Adjust the economic assumptions and compare **all three** approaches. The percentage of "
        "losses avoided is NOT the percentage of insects killed. Any difference among default "
        "strategies is caused by hypothetical inputs, not established biological superiority."
    )
    a, b, c, d, e = st.columns(5)
    with a:
        st.number_input("Acres", min_value=1, max_value=200, value=10, key="acres")
    with b:
        st.number_input("Yield (lb/acre)", min_value=1000, max_value=100000, value=30000, step=1000, key="yield_lb")
    with c:
        st.number_input("Price ($/lb)", min_value=0.10, max_value=10.0, value=0.80, step=0.05, key="price")
    with d:
        st.number_input("Management budget ($)", min_value=0, max_value=200000, value=8000, step=500, key="budget")
    with e:
        st.slider("Untreated revenue loss (%)", 0, 60, 20, key="loss_pct")
    gross = st.session_state.acres * st.session_state.yield_lb * st.session_state.price
    st.metric("Baseline gross revenue (not profit)", money(gross))
    results = []
    for i, strategy in enumerate(STRATEGIES):
        with st.expander(strategy, expanded=(i == 0)):
            left, right = st.columns(2)
            with left:
                st.slider("Additional management cost ($)", 0, 20000, DEFAULT_COSTS[i], 250, key=f"cost_{i}")
            with right:
                st.slider("Assumed share of losses avoided (%)", 0, 100, DEFAULT_AVOIDED[i], 5, key=f"avoided_{i}")
            st.caption("Document why these hypothetical assumptions are or are not credible in your final response.")
        cost = st.session_state[f"cost_{i}"]
        avoided = st.session_state[f"avoided_{i}"]
        threatened, preserved, net = calculate(gross, st.session_state.loss_pct, cost, avoided)
        results.append({
            "Strategy": strategy, "Cost ($)": cost, "Assumed losses avoided (%)": avoided,
            "Revenue preserved ($)": round(preserved), "Incremental benefit ($)": round(net),
            "Within budget": "Yes" if cost <= st.session_state.budget else "No",
        })
    results_df = pd.DataFrame(results)
    st.dataframe(results_df, use_container_width=True, hide_index=True)
    st.bar_chart(results_df.set_index("Strategy")["Incremental benefit ($)"])
    st.caption(
        "Model: gross = acres × yield × price; revenue preserved = gross × untreated-loss fraction × "
        "assumed losses-avoided fraction; incremental benefit = revenue preserved − management cost. "
        "Other production, harvest, packing, environmental, and market effects are excluded."
    )
    st.text_area("Which assumptions most strongly influence the ranking? What evidence would improve them?", key="economic_interpretation")

with tabs[2]:
    st.subheader("Consult the four AI stakeholders")
    st.write(
        "Open each Gem, propose your plan, and challenge its position. Return here to document "
        "one objection or constraint AND how you would respond. Gemini access and sharing "
        "permissions may be required; conversations are external to this app."
    )
    for name, (url, perspective, suggested_question) in GEMS.items():
        with st.container(border=True):
            st.markdown(f"#### {name}")
            st.caption(perspective)
            st.link_button("Open this stakeholder Gem", url)
            st.write(f"**Suggested opening question:** {suggested_question}")
            st.text_area("Main concern or objection", key=f"concern_{name}", height=80)
            st.text_area("My evidence-based reply or compromise", key=f"response_{name}", height=80)

with tabs[3]:
    st.subheader("Advance seven days: New field evidence")
    st.write("A week has passed. The first harvest is now about 14 days away.")
    if not st.session_state.locked:
        st.warning("Lock your initial prediction on Tab 1 before revealing the update.")
    elif not st.session_state.update_revealed:
        st.info("Your initial prediction is protected. Click below to see the next scouting report.")
        if st.button("Advance seven days — reveal new evidence", type="primary"):
            st.session_state.update_revealed = True
            st.rerun()
    else:
        st.success("Seven-day report revealed")
        st.write(
            "Scouting indicates a higher concentration of whiteflies along one field margin than "
            "in the interior. These values are new **hypothetical** observations, not a prediction "
            "of what your selected treatment would produce."
        )
        st.dataframe(UPDATE_DATA, use_container_width=True, hide_index=True)
        st.bar_chart(UPDATE_DATA.set_index("Field zone")[[
            "Adult whiteflies / sampled leaf", "Nymphs / sampled leaf"
        ]])
        st.info(
            "A buyer also asks whether the field can meet the agreed delivery date. "
            "Before choosing any pesticide, verify the label, preharvest interval (PHI), "
            "restricted-entry interval (REI), resistance considerations, and buyer specifications."
        )
        st.text_area(
            "How does this new spatial information change your assessment? "
            "Would you sample more, consider targeted management, or revise your strategy—and why?",
            key="update_interpretation", height=130,
        )

with tabs[4]:
    st.subheader("Revise and defend your management recommendation")
    if st.session_state.locked:
        st.write("**Your locked prediction:**", st.session_state.initial_strategy_locked)
        st.info(st.session_state.initial_reason_locked)
    else:
        st.warning("Complete the initial prediction first.")
    if not st.session_state.update_revealed:
        st.warning("Reveal the seven-day update before completing your final decision.")
    st.selectbox("Final proposed strategy", STRATEGIES, key="final_strategy")
    st.text_area("Biological evidence: Explain scouting trends, field distribution, symptoms and unknowns.", key="final_biology", height=100)
    st.text_area("Economic reasoning: Compare alternatives, include assumptions and budget feasibility.", key="final_economics", height=100)
    st.text_area("What evidence or stakeholder objection changed or strengthened your reasoning?", key="reasoning_change", height=100)
    st.text_area("What major uncertainty remains, and what evidence would change your recommendation?", key="final_uncertainty", height=90)
    st.text_area(
        "Feasibility: Address harvest timing, PHI/REI, prior mode of action, buyer requirements, "
        "and what must be verified before an actual treatment.", key="feasibility", height=100
    )
    if st.session_state.locked:
        st.markdown(
            f"**Initial:** {st.session_state.initial_strategy_locked}  "
            f"→ **Final:** {st.session_state.final_strategy}"
        )

with tabs[5]:
    st.subheader("Criterion-based reflection and export")
    st.write("This is a self-review, not an automated correctness grade. Another student or instructor should challenge your justification.")
    st.checkbox("My decision uses scouting observations, pest biology and uncertainty", key="rubric_biology")
    st.checkbox("I compared costs, assumptions and potential economic benefits", key="rubric_economics")
    st.checkbox("I addressed a specific objection from each of the four stakeholders", key="rubric_stakeholders")
    st.checkbox("I explained how new information changed or strengthened my position", key="rubric_revision")
    if st.button("Check submission completeness", type="primary"):
        missing = []
        if not st.session_state.locked:
            missing.append("Lock your initial prediction (Tab 1).")
        if not st.session_state.update_revealed:
            missing.append("Reveal the seven-day report (Tab 4).")
        if not st.session_state.get("update_interpretation", "").strip():
            missing.append("Interpret the new scouting evidence (Tab 4).")
        for name in GEMS:
            if not st.session_state.get(f"concern_{name}", "").strip() or not st.session_state.get(f"response_{name}", "").strip():
                missing.append(f"Document both fields for {name} (Tab 3).")
        for key, label in [
            ("final_biology", "biological evidence"), ("final_economics", "economic reasoning"),
            ("reasoning_change", "revised reasoning"), ("final_uncertainty", "uncertainty"),
            ("feasibility", "feasibility"),
        ]:
            if not st.session_state.get(key, "").strip():
                missing.append(f"Complete the final {label} response (Tab 5).")
        for key in ("rubric_biology", "rubric_economics", "rubric_stakeholders", "rubric_revision"):
            if not st.session_state.get(key, False):
                missing.append("Complete all four self-review checks.")
                break
        if missing:
            st.warning("Still to complete (this does NOT assess scientific correctness):")
            for issue in missing:
                st.write("•", issue)
        else:
            st.success("All required fields are complete. Have an instructor or peer evaluate scientific accuracy.")
    st.download_button(
        "Download all responses and assumptions (CSV)", data=export_csv(),
        file_name="hort2000_tomato_decision_v2.csv", mime="text/csv",
    )
    if st.session_state.locked:
        st.write("**Initial:**", st.session_state.initial_strategy_locked)
        st.write("**Final:**", st.session_state.get("final_strategy", "Not chosen"))

st.divider()
st.caption(
    "Background: UGA CAES Commercial Tomato Production Handbook (historical): "
    "https://fieldreport.caes.uga.edu/publications/B1312/commercial-tomato-production-handbook/ "
    "| Current UGA pest guidance: https://ipm.uga.edu/georgia-pest-management-handbook/ "
    "| Consult current product labels before any real intervention."
)
