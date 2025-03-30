# app.py

import streamlit as st
from tone_rewriter import ToneRewriter
from emotion_detector import EmotionDetector

st.set_page_config(page_title="TonePolish", layout="centered")
st.title("📝 TonePolish")
st.subheader("Tone-Aware Text Rewriter for Professional English Communication")

@st.cache_resource
def load_models():
    return EmotionDetector(), ToneRewriter()

emotion_model, rewriter_model = load_models()

text = st.text_area("✏️ Enter your sentence", height=150)
tone = st.selectbox("🎯 Desired Tone", ["friendly", "confident", "humble", "formal"])

if st.button("🔁 Rewrite"):
    if not text.strip():
        st.warning("Please enter some text.")
    else:
        with st.spinner("Analyzing emotion..."):
            emotion = emotion_model.detect(text)

        if "error" in emotion:
            st.error(f"Emotion Detection Error: {emotion['error']}")
        else:
            st.success(f"Detected Emotion: `{emotion['emotion']}` with confidence `{emotion['confidence']}`")

            with st.spinner("Rewriting in selected tone..."):
                rewritten = rewriter_model.rewrite(text, tone=tone)

            if "error" in rewritten:
                st.error(f"Tone Rewriting Error: {rewritten['error']}")
            else:
                st.subheader("📤 Output")
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**Original**")
                    st.write(text)
                with col2:
                    st.markdown("**Rewritten**")
                    st.write(rewritten["rewritten"])
