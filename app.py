import streamlit as st

from src.pipeline import evaluate_student
from src.dataset_metadata import TOPIC_OPTIONS, get_expected_concepts

TOPIC_CONCEPTS = {
    "Overfitting": "training performance;test performance;noise",
    "Underfitting": "training performance;test performance;model complexity",
    "Bias-Variance": "bias;variance;generalization;training error;test error",
    "Generalization": "training data;unseen data;test performance;noise",
}


def metric_status(score):
    if score >= 80:
        return "good"
    if score >= 60:
        return "warning"
    return "needs-work"

st.set_page_config(page_title="MindCheck AI", page_icon="🧠", layout="wide")

st.markdown(
    """
    <style>
    html, body, [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #f8fbff 0%, #eef5ff 55%, #f7fbff 100%);
        color: #172b57;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1500px;
    }
    .stAppHeader {
        background: rgba(255, 255, 255, 0.86);
        border-bottom: 1px solid #e5edf8;
    }
    [data-testid="stDeployButton"] {
        display: none !important;
    }
    h1, h2, h3, h4, p, label, [data-testid="stMetricLabel"] {
        color: #172b57 !important;
    }
    h1 {
        font-size: 2.1rem !important;
        letter-spacing: -0.02em;
    }
    h2, h3 {
        letter-spacing: -0.015em;
    }
    .stMetric {
        background: rgba(255, 255, 255, 0.86);
        border: 1px solid #dfe9f7;
        border-radius: 0.9rem;
        padding: 1rem 1.1rem;
        box-shadow: 0 8px 24px rgba(76, 117, 178, 0.09);
    }
    .metric-card {
        background: rgba(255, 255, 255, 0.9);
        border: 1px solid var(--metric-border);
        border-top: 5px solid var(--metric-color);
        border-radius: 0.9rem;
        padding: 1rem 1.1rem;
        box-shadow: 0 8px 24px rgba(76, 117, 178, 0.09);
    }
    .metric-card.good {
        --metric-color: #18864b;
        --metric-border: #a9e3bd;
    }
    .metric-card.warning {
        --metric-color: #b77900;
        --metric-border: #f6d48a;
    }
    .metric-card.needs-work {
        --metric-color: #bd3045;
        --metric-border: #f5b7c0;
    }
    .metric-label {
        color: #59739d;
        font-size: 0.85rem;
        font-weight: 700;
    }
    .metric-value {
        color: var(--metric-color);
        font-size: 1.75rem;
        font-weight: 800;
        line-height: 1.2;
        margin-top: 0.25rem;
    }
    div[data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.94);
        border-right: 1px solid #e1eaf6;
    }
    div[data-testid="stForm"] {
        background: rgba(255, 255, 255, 0.9);
        border: 1px solid #e0e9f6;
        border-radius: 1rem;
        padding: 1.25rem 1.35rem;
        box-shadow: 0 14px 35px rgba(72, 111, 170, 0.1);
    }
    textarea, input, select {
        border-radius: 0.7rem !important;
        background: #ffffff !important;
        color: #263d68 !important;
        border: 1px solid #d4e1f2 !important;
    }
    textarea:focus, input:focus {
        border-color: #2f76ed !important;
        box-shadow: 0 0 0 2px rgba(47, 118, 237, 0.13) !important;
    }
    .stButton > button {
        border-radius: 0.65rem;
        font-weight: 700;
        background: linear-gradient(135deg, #0f8b8d, #22b8a7);
        color: white;
        border: none;
        padding: 0.8rem 1.2rem;
        box-shadow: 0 8px 18px rgba(15, 139, 141, 0.25);
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #0b7072, #189987);
    }
    .stAlert {
        border-radius: 0.75rem;
    }
    .stCode {
        border-radius: 0.8rem;
        background: #f1f6fd;
        border: 1px solid #dce7f5;
    }
    .concept-chip {
        display: inline-block;
        padding: 0.45rem 0.8rem;
        margin: 0.25rem 0.35rem 0.25rem 0;
        border-radius: 999px;
        background: #eaf3ff;
        border: 1px solid #cfe2fb;
        color: #2a62b4;
        font-size: 0.85rem;
    }
    .mistake-card {
        background: #fff1f3;
        border: 1px solid #ffcbd2;
        border-radius: 1rem;
        padding: 1rem;
    }
    .answer-status {
        border-radius: 0.8rem;
        padding: 0.9rem 1.1rem;
        margin: 0.6rem 0 1rem;
        font-weight: 700;
    }
    .answer-status.correct {
        background: #eaf9f0;
        border: 1px solid #a9e3bd;
        color: #187b42;
    }
    .answer-status.partial {
        background: #fff7e5;
        border: 1px solid #f6d48a;
        color: #9a6500;
    }
    .answer-status.incorrect {
        background: #fff0f2;
        border: 1px solid #f5b7c0;
        color: #bd3045;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("MindCheck AI")
st.caption("Understand the student's reasoning, detect misconceptions, and guide learning.")

st.markdown(
    """
    <div style='background: linear-gradient(135deg, #edf5ff, #f8fbff); border:1px solid #d9e7f8; border-radius:1.2rem; padding:1.5rem; margin-bottom:1.25rem; box-shadow:0 12px 30px rgba(72,111,170,0.08);'>
      <div style='display:flex; justify-content:space-between; align-items:center; gap:1rem; flex-wrap:wrap;'>
        <div>
          <p style='margin:0 0 0.4rem 0; font-size:0.8rem; letter-spacing:0.12em; text-transform:uppercase; color:#3479dd;'>AI Learning Lab</p>
          <h2 style='margin:0; font-size:2.2rem;'>Misconception-Aware Tutor</h2>
        </div>
        <div style='background:#ffffff; border:1px solid #d9e7f8; border-radius:0.9rem; padding:0.7rem 1rem; color:#23406f; box-shadow:0 6px 16px rgba(72,111,170,0.08);'>
          <strong>Demo-ready</strong><br>
          <span style='opacity:0.7;'>Concept analysis + feedback</span>
        </div>
      </div>
    <p style='margin-top:1rem; max-width:900px; color:#59739d;'>This system checks how a student understands a concept, detects confusion patterns, and gives targeted feedback instead of only marking the answer correct or wrong.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

concept_coverage = 0
misconception_detection = 0
feedback_quality_score = 0
metric_cols = st.columns(3)
with metric_cols[0]:
    st.markdown(
        f"<div class='metric-card {metric_status(concept_coverage)}'><div class='metric-label'>Concept Coverage</div><div class='metric-value'>{concept_coverage}%</div></div>",
        unsafe_allow_html=True,
    )
with metric_cols[1]:
    st.markdown(
        f"<div class='metric-card {metric_status(misconception_detection)}'><div class='metric-label'>Misconception Detection</div><div class='metric-value'>{misconception_detection}%</div></div>",
        unsafe_allow_html=True,
    )
with metric_cols[2]:
    st.markdown(
        f"<div class='metric-card {metric_status(feedback_quality_score)}'><div class='metric-label'>Feedback Quality</div><div class='metric-value'>{feedback_quality_score}%</div></div>",
        unsafe_allow_html=True,
    )

st.markdown("---")

with st.form("tutor_form"):
    left_col, right_col = st.columns([1.4, 1])

    with left_col:
        topic = st.selectbox("Topic", TOPIC_OPTIONS, index=0, key="topic")
        question = st.text_area(
            "Question",
            height=160,
            key="question",
            help="Type or edit the question here.",
        )

        student_answer = st.text_area(
            "Student answer",
            height=220,
            key="student_answer",
            help="Write the student's answer here.",
        )

    with right_col:
        st.markdown("### Expected Concepts")
        target_text = st.session_state.get("expected_concepts", get_expected_concepts(topic))
        expected_concepts = st.text_area(
            "Expected concept keywords",
            value=target_text,
            height=150,
            key="expected_concepts",
            help="Example: training performance;test performance;noise",
        )

        st.markdown("### Learning Hint")
        st.info("Look for the difference between performance on training data and performance on unseen data.")

        st.markdown("### Live concept chips")
        concept_items = [
            "training performance",
            "test performance",
            "generalization",
            "noise",
        ]
        st.markdown(
            "".join(f"<span class='concept-chip'>{item}</span>" for item in concept_items),
            unsafe_allow_html=True,
        )

    submitted = st.form_submit_button("Analyze Answer", use_container_width=True)

if submitted:
    if not question.strip() or not student_answer.strip():
        st.warning("Please provide both the question and the student's answer.")
    else:
        result = evaluate_student(question, expected_concepts, student_answer, topic)

        st.markdown("### Analysis Dashboard")
        status_class = {
            "Correct": "correct",
            "Partially Correct": "partial",
            "Incorrect": "incorrect",
        }.get(result["label"], "incorrect")
        status_icon = {
            "Correct": "✓",
            "Partially Correct": "!",
            "Incorrect": "×",
        }.get(result["label"], "×")
        st.markdown(
            f"<div class='answer-status {status_class}'>{status_icon} &nbsp;{result['label']}</div>",
            unsafe_allow_html=True,
        )
        col1, col2, col3 = st.columns(3)
        col1.metric("Classification", result["label"])
        col2.metric("Coverage", f"{result['coverage'] * 100:.0f}%")
        col3.metric("Misconception", result["misconception"])
        training = result["training"]
        learned_label = result["model_prediction"] or "Unavailable"
        learned_confidence = result["model_confidence"] * 100
        st.caption(
            f"Dataset-trained signal: {learned_label} ({learned_confidence:.0f}% confidence) "
            f"from {training['example_count']} labeled examples."
        )

        st.markdown("### Concept Match")
        c1, c2 = st.columns(2)
        with c1:
            st.info(f"Matched concepts: {result['matched'] if result['matched'] else 'None'}")
        with c2:
            st.info(f"Missing concepts: {result['missing'] if result['missing'] else 'None'}")

        st.markdown("### Misconception Card")
        if result["misconception"] == "None":
            st.success("No major misconception detected.")
        else:
            st.markdown(
                f"<div class='mistake-card'><strong>Possible misconception:</strong> {result['misconception']}</div>",
                unsafe_allow_html=True,
            )

        st.markdown("### Tutor Feedback")
        if result["label"] == "Correct":
            st.success(result["feedback"])
        elif result["label"] == "Partially Correct":
            st.warning(result["feedback"])
        else:
            st.error(result["feedback"])

        with st.expander("How the model works"):
            st.markdown(
                """
                - Concept coverage checks whether the answer includes the required ideas.
                - Contradiction detection catches common confusion such as overfitting vs underfitting.
                - Missing concepts are highlighted as gaps in understanding.
                - Misconception tags help provide personalized learning guidance.
                """
            )

        with st.expander("Sample answers"):
            st.code(
                """Correct: Overfitting happens when a model learns the training data too closely and performs poorly on new, unseen data.
Incorrect: Overfitting occurs when the model performs poorly on both the training data and testing data.
Partially correct: Overfitting is when the model does well on training data but not on test data.""",
                language="text",
            )
