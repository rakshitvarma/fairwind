"""RouteWise demo — live showcase of the Track 1 routing agent.

Reuses the exact same router package (classifier, solvers, fireworks_client)
that runs inside the submitted Docker image, so this demo reflects real
behavior rather than a reimplementation.
"""
import os
import sys
import time

import streamlit as st

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from router.classifier import classify
from router.solvers import try_solve_math
from router.fireworks_client import FireworksClient

st.set_page_config(page_title="RouteWise", page_icon="🧭", layout="centered")

# Bridge Streamlit secrets into the environment variables FireworksClient
# reads, without touching the router package used by the submitted image.
for key in ("FIREWORKS_API_KEY", "FIREWORKS_BASE_URL", "ALLOWED_MODELS"):
    if key not in os.environ and key in st.secrets:
        os.environ[key] = st.secrets[key]

CATEGORY_COLOR = {
    "math": "#7C5CFC",
    "factual": "#5CC8FC",
    "sentiment": "#FC5C8D",
    "summarization": "#5CFCA8",
    "ner": "#FCC85C",
    "code_debug": "#FC8D5C",
    "code_gen": "#8D5CFC",
    "logic": "#5CFCE0",
}

EXAMPLES = {
    "Math": "A store marks up a $40 item by 30% and then offers a 10% discount on the marked-up price. What is the final price?",
    "Factual": "Explain what a black hole is in simple terms.",
    "Sentiment": "Classify the sentiment: 'The food was okay, nothing special, but the service was excellent.'",
    "Summarization": "Summarise the following in one short sentence: Researchers found that participants who slept less than six hours a night for a week showed slower reaction times and reduced memory recall compared to a control group that slept eight hours.",
    "NER": "Extract all named entities from: 'Marie Curie won the Nobel Prize in Physics in 1903 while working in Paris.'",
    "Code debug": "Find and fix the bug: ```def is_even(n):\n    return n % 2 == 1```",
    "Code gen": "Write a Python function is_palindrome(s) that returns True if a string reads the same forwards and backwards, ignoring case and spaces.",
    "Logic": "Three boxes are labeled 'Apples', 'Oranges', and 'Mixed', but all labels are wrong. You may pick one fruit from one box to determine the correct labels. Which box should you pick from, and why?",
}

st.markdown(
    """
    <style>
    .rw-badge {
        display: inline-block; padding: 3px 12px; border-radius: 999px;
        font-size: 0.8rem; font-weight: 600; color: #0E1117;
    }
    .rw-card {
        background: #171A23; border-radius: 14px; padding: 1.2rem 1.4rem;
        border: 1px solid #262B3A; margin-top: 0.8rem;
    }
    .rw-metric { color: #9AA0AE; font-size: 0.85rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🧭 RouteWise")
st.caption(
    "Hybrid token-efficient routing agent — built for AMD Developer Hackathon "
    "Act II, Track 1. Classifies and solves for free where it can, and only "
    "pays for Fireworks inference on tasks that genuinely need it."
)

if "history" not in st.session_state:
    st.session_state.history = []
if "total_tokens" not in st.session_state:
    st.session_state.total_tokens = 0

with st.sidebar:
    st.subheader("How it works")
    st.markdown(
        "1. **Local classifier** (regex, 0 tokens) routes the task into one "
        "of 8 categories.\n"
        "2. **Deterministic math solver** answers bare arithmetic instantly "
        "for free — word problems fall through to Fireworks.\n"
        "3. **Logic puzzles** get 3-call self-consistency (majority vote) — "
        "cheap insurance against a demonstrated flaky-reasoning failure mode.\n"
        "4. **Everything else** is merged by model into as few Fireworks "
        "calls as possible (not one call per category)."
    )
    st.divider()
    tokens_metric = st.empty()
    tokens_metric.metric("Session tokens spent", st.session_state.total_tokens)
    st.divider()
    st.markdown(
        "[GitHub repo](https://github.com/rakshitvarma/routewise) · "
        "[Docker image](https://github.com/rakshitvarma/routewise/pkgs/container/routewise)"
    )

st.subheader("Try it")
cols = st.columns(4)
for i, (label, prompt) in enumerate(EXAMPLES.items()):
    if cols[i % 4].button(label, use_container_width=True):
        st.session_state.prompt_input = prompt

prompt = st.text_area(
    "Task prompt", key="prompt_input", height=100,
    placeholder="Type a task, or click an example above...",
)
run = st.button("Route & Answer", type="primary")

has_creds = all(os.environ.get(k) for k in ("FIREWORKS_API_KEY", "FIREWORKS_BASE_URL", "ALLOWED_MODELS"))
if not has_creds:
    st.info(
        "Fireworks credentials aren't configured for this demo instance, so only "
        "the zero-token local paths (math, classification) will run live. "
        "Everything else will show the routing decision without a live answer.",
        icon="ℹ️",
    )

if run and prompt.strip():
    category = classify(prompt)
    color = CATEGORY_COLOR.get(category, "#9AA0AE")
    started = time.time()

    local_answer = try_solve_math(prompt) if category == "math" else None

    answer, model_used, tokens_used = None, None, 0
    if local_answer is not None:
        answer, model_used = local_answer, "local (deterministic)"
    elif has_creds:
        try:
            client = FireworksClient()
            if category == "logic":
                model_used = client.pick_model("logic")
                answer = client._answer_logic(model_used, prompt)
            else:
                result = client.answer_all({category: [("live", prompt)]})
                answer = result.get("live", "")
                model_used = client.pick_model(category)
            tokens_used = client.total_tokens
            st.session_state.total_tokens += tokens_used
            tokens_metric.metric("Session tokens spent", st.session_state.total_tokens)
        except Exception as exc:
            answer = f"(Fireworks call failed: {exc})"
            model_used = "error"
    else:
        answer, model_used = "(no live credentials configured for this demo)", "n/a"

    elapsed = time.time() - started

    st.markdown(
        f'<div class="rw-card">'
        f'<span class="rw-badge" style="background:{color}">{category}</span>'
        f'&nbsp;&nbsp;<span class="rw-metric">{model_used} · {tokens_used} tokens · {elapsed:.1f}s</span>'
        f'<hr style="border-color:#262B3A">'
        f'<div style="white-space:pre-wrap">{answer}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    st.session_state.history.insert(0, {
        "prompt": prompt[:60] + ("…" if len(prompt) > 60 else ""),
        "category": category,
        "source": model_used,
        "tokens": tokens_used,
    })

if st.session_state.history:
    st.subheader("Session history")
    st.dataframe(st.session_state.history, use_container_width=True, hide_index=True)
