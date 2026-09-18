import streamlit as st

from src.pipeline import evaluate_student
from src.dataset_metadata import TOPIC_OPTIONS, get_expected_concepts

def metric_status(score):
    if score >= 80:
        return "good"
    if score >= 60:
        return "warning"
    return "needs-work"

st.set_page_config(page_title="MindCheck AI", page_icon="✨", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    /* Classy, professional, soothing light gradient */
    background: linear-gradient(-45deg, #F8FAFC, #EEF2FF, #F1F5F9, #E0E7FF);
    background-size: 400% 400%;
    animation: gradientBG 20s ease infinite;
    color: #0F172A;
    font-family: 'Outfit', sans-serif;
}

@keyframes gradientBG {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 3rem;
    max-width: 1400px;
}
h1, h2, h3, h4, p, label, [data-testid="stMetricLabel"] {
    color: #0F172A !important;
    font-family: 'Outfit', sans-serif;
}

/* Professional Hero Title - Standalone */
.hero-section {
    text-align: center;
    margin-bottom: 2rem;
    padding-top: 1rem;
    animation: fadeInDown 0.8s ease-out;
}
.flashy-title {
    margin: 0;
    font-size: 4.5rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    background: linear-gradient(135deg, #0F172A 0%, #3B82F6 50%, #0F172A 100%);
    background-size: 200% auto;
    color: #fff;
    background-clip: text;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: subtleShine 6s linear infinite;
    filter: drop-shadow(0 4px 10px rgba(59, 130, 246, 0.15));
}
.hero-subtitle {
    font-size: 1.15rem;
    color: #475569 !important;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    font-weight: 600;
    margin-top: 0.5rem;
}

@keyframes subtleShine {
    to { background-position: 200% center; }
}
@keyframes fadeInDown {
    from { opacity: 0; transform: translateY(-20px); }
    to { opacity: 1; transform: translateY(0); }
}

/* Classy White Cards with subtle elegant borders */
.metric-card {
    background: #ffffff;
    border: 1px solid rgba(226, 232, 240, 0.8);
    border-radius: 1rem;
    padding: 1.5rem;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.03);
    transition: all 0.3s ease;
}
.metric-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 15px 40px rgba(0, 0, 0, 0.06);
    border-color: #CBD5E1;
}
.metric-card.good { --metric-color: #059669; }
.metric-card.warning { --metric-color: #D97706; }
.metric-card.needs-work { --metric-color: #DC2626; } 

.metric-label {
    color: #64748B;
    font-size: 0.85rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
.metric-value {
    color: var(--metric-color);
    font-size: 2.2rem;
    font-weight: 700;
    line-height: 1.2;
    margin-top: 0.25rem;
}

div[data-testid="stForm"] {
    background: #ffffff;
    border: 1px solid rgba(226, 232, 240, 0.8);
    border-radius: 1.2rem;
    padding: 2.5rem;
    box-shadow: 0 15px 40px rgba(0, 0, 0, 0.03);
}

/* Professional Inputs */
textarea, input, select {
    border-radius: 0.5rem !important;
    background: #F8FAFC !important;
    color: #0F172A !important;
    border: 1px solid #CBD5E1 !important;
    transition: all 0.2s ease !important;
    box-shadow: none !important;
    font-size: 1rem !important;
}
textarea:focus, input:focus, select:focus {
    border-color: #3B82F6 !important;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15) !important;
    background: #FFFFFF !important;
}

/* Classy Corporate Button */
div[data-testid="stButton"] > button {
    border-radius: 0.5rem !important;
    font-weight: 600 !important;
    background-color: #2563EB !important;
    background-image: none !important;
    border: none !important;
    padding: 0.8rem 1.5rem !important;
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2) !important;
    transition: all 0.2s ease !important;
    letter-spacing: 0.5px !important;
    color: #ffffff !important;
}
div[data-testid="stButton"] > button * {
    color: #ffffff !important;
    font-size: 1.05rem !important;
}
div[data-testid="stButton"] > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 16px rgba(37, 99, 235, 0.3) !important;
    background-color: #1D4ED8 !important;
}

/* Elegant Chips */
.concept-chip {
    display: inline-block;
    padding: 0.4rem 1rem;
    margin: 0.25rem 0.25rem 0.25rem 0;
    border-radius: 0.4rem;
    background: #F1F5F9;
    border: 1px solid #E2E8F0;
    color: #334155;
    font-size: 0.85rem;
    font-weight: 500;
}

/* Status Cards */
.mistake-card {
    background: #FEF2F2;
    border: 1px solid #FCA5A5;
    border-left: 4px solid #DC2626;
    border-radius: 0.75rem;
    padding: 1.5rem;
}
.answer-status {
    border-radius: 0.75rem;
    padding: 1.2rem 1.5rem;
    margin: 0.6rem 0 1.2rem;
    font-weight: 600;
    font-size: 1.1rem;
    display: flex;
    align-items: center;
    gap: 0.75rem;
    background: #ffffff;
    border: 1px solid rgba(226, 232, 240, 0.8);
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.02);
}
.answer-status.correct { color: #059669; border-left: 4px solid #059669; }
.answer-status.partial { color: #D97706; border-left: 4px solid #D97706; }
.answer-status.incorrect { color: #DC2626; border-left: 4px solid #DC2626; }

/* Description Banner (No longer containing the main title) */
.banner-container {
    background: #ffffff;
    border: 1px solid rgba(226, 232, 240, 0.8);
    border-radius: 1rem;
    padding: 2rem;
    margin-bottom: 2.5rem;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.03);
    display: flex;
    justify-content: center;
    align-items: center;
}
.banner-text {
    max-width: 900px;
    color: #475569;
    font-size: 1.1rem;
    line-height: 1.7;
    text-align: center;
    margin: 0;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class='hero-section'>
    <h1 class='flashy-title'>MINDCHECK AI</h1>
    <p class='hero-subtitle'>Next-Gen Misconception-Aware Tutor</p>
</div>

<div class='banner-container'>
    <p class='banner-text'>This system evaluates student understanding by detecting underlying confusion patterns and providing targeted, pedagogical feedback—moving beyond simple correct/incorrect grading.</p>
</div>
""", unsafe_allow_html=True)

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

st.markdown("<br>", unsafe_allow_html=True)

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
