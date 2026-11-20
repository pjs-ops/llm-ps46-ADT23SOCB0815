import json
import os
import sys
from datetime import date
from pathlib import Path

import pandas as pd
import streamlit as st
from dotenv import load_dotenv

# Robust .env loading from current file directory or current working directory
env_path = Path(__file__).resolve().parent / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path, override=True)
else:
    load_dotenv(override=True)

# Try importing the official Groq SDK; fallback to requests if unavailable
try:
    from groq import (
        APIConnectionError,
        APIStatusError,
        AuthenticationError,
        BadRequestError,
        Groq,
        InternalServerError,
        NotFoundError,
        PermissionDeniedError,
        RateLimitError,
    )
    GROQ_SDK_AVAILABLE = True
except ImportError:
    import requests
    GROQ_SDK_AVAILABLE = False


# Streamlit Page Setup
st.set_page_config(
    page_title="TaskWise AI · Smart To-Do Generator",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Soft, Elegant Pastel Blue, Beige & Warm Yellow Custom CSS
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=Playfair+Display:ital,wght@0,600;0,700;1,600&family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200&display=swap');

/* Global Reset & Typography - targeted to text containers only */
html, body, .stApp, .stMarkdown, p, h1, h2, h3, h4, h5, h6, label, input, textarea, select {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    color: #3E4A59;
}

/* Ensure Material Symbols and Streamlit icons always retain their icon font */
[data-testid="stIconMaterial"],
span[data-testid="stIconMaterial"],
.material-symbols-rounded,
.material-icons,
[data-testid="stSidebarCollapseButton"] span,
[data-testid="stSidebarCollapsedControl"] span {
    font-family: 'Material Symbols Rounded', 'Material Icons' !important;
    font-weight: normal !important;
    font-style: normal !important;
    font-size: 20px !important;
    line-height: 1 !important;
    letter-spacing: normal !important;
    text-transform: none !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    white-space: nowrap !important;
    word-wrap: normal !important;
    direction: ltr !important;
    font-feature-settings: 'liga' 1 !important;
    -webkit-font-feature-settings: 'liga' 1 !important;
    -webkit-font-smoothing: antialiased !important;
}

/* Sidebar Collapse & Expand Toggle Buttons */
[data-testid="stSidebarCollapseButton"] button,
[data-testid="stSidebarCollapsedControl"] button {
    background-color: transparent !important;
    border: none !important;
    color: #3E4A59 !important;
    border-radius: 8px !important;
    padding: 6px !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    transition: all 0.2s ease !important;
}

[data-testid="stSidebarCollapseButton"] button:hover,
[data-testid="stSidebarCollapsedControl"] button:hover {
    background-color: #EADCCF !important;
    color: #194666 !important;
}

/* Force light pastel background across the app */
.stApp {
    background: #FAF7F0 !important;
    color: #3E4A59 !important;
}

/* Explicit text color override for all headings and paragraphs */
h1, h2, h3, h4, h5, h6, p, label {
    color: #3E4A59;
}

/* Header Banner Section */
.main-header {
    background: linear-gradient(135deg, #DCEEFF 0%, #FAF7F0 50%, #F7E7A8 100%);
    border: 1.5px solid #D5E5F2;
    border-radius: 22px;
    padding: 26px 32px;
    margin-bottom: 24px;
    box-shadow: 0 8px 24px rgba(141, 191, 217, 0.16);
}

.main-title {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 2.25rem;
    font-weight: 700;
    color: #243E56;
    margin: 0;
    display: flex;
    align-items: center;
    gap: 12px;
}

.sub-title {
    font-size: 1.02rem;
    color: #5C6E82;
    margin-top: 6px;
    line-height: 1.5;
}

.badge-row {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 14px;
}

.pill-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 5px 14px;
    border-radius: 999px;
    font-size: 0.82rem;
    font-weight: 600;
}

.pill-roll {
    background: #EADCCF;
    color: #553E2D;
    border: 1px solid #D8C7B5;
}

.pill-model {
    background: #CFE8F7;
    color: #194666;
    border: 1px solid #B5DAF2;
}

.pill-date {
    background: #F7E7A8;
    color: #5E4705;
    border: 1px solid #E8D385;
}

/* Soft Dashboard Metric Cards */
.stats-container {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
    gap: 14px;
    margin-bottom: 22px;
}

.stat-card {
    background: #FFFDF8;
    border: 1.5px solid #E5DDD3;
    border-radius: 16px;
    padding: 16px;
    text-align: center;
    box-shadow: 0 3px 12px rgba(229, 221, 211, 0.4);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.stat-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 18px rgba(141, 191, 217, 0.2);
    border-color: #8DBFD9;
}

.stat-val {
    font-size: 1.65rem;
    font-weight: 700;
    color: #2F5275;
    line-height: 1.2;
}

.stat-lbl {
    font-size: 0.78rem;
    font-weight: 700;
    color: #6B7280;
    text-transform: uppercase;
    letter-spacing: 0.6px;
    margin-top: 5px;
}

/* Task Card Styling */
.task-card {
    background: #FFFDF8;
    border: 1.5px solid #E5DDD3;
    border-radius: 16px;
    padding: 15px 20px;
    margin-bottom: 12px;
    box-shadow: 0 3px 10px rgba(141, 191, 217, 0.08);
    transition: all 0.2s ease;
}

.task-card:hover {
    box-shadow: 0 6px 18px rgba(141, 191, 217, 0.18);
    border-color: #8DBFD9;
}

.task-completed {
    background: #F4EFE6 !important;
    opacity: 0.72;
    border-color: #E0D7CC !important;
}

.task-completed .task-text {
    text-decoration: line-through;
    color: #8C96A3 !important;
}

.task-text {
    font-size: 1.02rem;
    font-weight: 600;
    color: #3E4A59;
}

/* Priority Badges - Soft Coral, Muted Golden Yellow, Soft Pastel Green */
.badge-priority-high {
    background: #FDE8E8;
    color: #C53047;
    border: 1px solid #FAC7CE;
    padding: 4px 12px;
    border-radius: 999px;
    font-size: 0.8rem;
    font-weight: 700;
    display: inline-block;
}

.badge-priority-med {
    background: #FEF3C7;
    color: #9A6700;
    border: 1px solid #FDE68A;
    padding: 4px 12px;
    border-radius: 999px;
    font-size: 0.8rem;
    font-weight: 700;
    display: inline-block;
}

.badge-priority-low {
    background: #E6F4EA;
    color: #1E6B3E;
    border: 1px solid #CEEAD6;
    padding: 4px 12px;
    border-radius: 999px;
    font-size: 0.8rem;
    font-weight: 700;
    display: inline-block;
}

/* Date / Deadline Badge - Soft Pastel Blue */
.badge-deadline {
    background: #DCEEFF;
    color: #215A85;
    border: 1px solid #C4E2FC;
    padding: 4px 12px;
    border-radius: 999px;
    font-size: 0.82rem;
    font-weight: 600;
    display: inline-block;
}

/* Sidebar Custom Styling */
[data-testid="stSidebar"] {
    background-color: #F8F5EE !important;
    border-right: 1.5px solid #E5DDD3 !important;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stMarkdown {
    color: #3E4A59 !important;
}

[data-testid="stSidebar"] .stTextInput input,
[data-testid="stSidebar"] .stSelectbox > div > div {
    background-color: #FFFDF8 !important;
    color: #3E4A59 !important;
    border: 1.5px solid #E5DDD3 !important;
    border-radius: 12px !important;
}

/* Text Area Aesthetics */
.stTextArea textarea {
    background-color: #FFFDF8 !important;
    color: #3E4A59 !important;
    border: 1.5px solid #E5DDD3 !important;
    border-radius: 16px !important;
    box-shadow: 0 2px 8px rgba(141, 191, 217, 0.08) !important;
    font-size: 0.98rem !important;
}

.stTextArea textarea:focus {
    border-color: #8DBFD9 !important;
    box-shadow: 0 0 0 3px rgba(141, 191, 217, 0.25) !important;
    outline: none !important;
}

/* Primary Button - Accent Pastel Blue */
.stButton button[kind="primary"] {
    background: linear-gradient(135deg, #8DBFD9 0%, #74AECB 100%) !important;
    color: #FFFFFF !important;
    border: 1px solid #74AECB !important;
    border-radius: 14px !important;
    font-weight: 700 !important;
    font-size: 0.98rem !important;
    padding: 10px 24px !important;
    box-shadow: 0 4px 14px rgba(116, 174, 203, 0.35) !important;
    transition: all 0.2s ease !important;
}

.stButton button[kind="primary"]:hover {
    background: linear-gradient(135deg, #74AECB 0%, #5E9AB9 100%) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 18px rgba(116, 174, 203, 0.45) !important;
}

/* Secondary Buttons - Cream & Beige with Soft Blue Hover */
.stButton button:not([kind="primary"]) {
    background-color: #FFFDF8 !important;
    color: #3E4A59 !important;
    border: 1.5px solid #E5DDD3 !important;
    border-radius: 14px !important;
    font-weight: 600 !important;
    box-shadow: 0 2px 6px rgba(229, 221, 211, 0.4) !important;
    transition: all 0.2s ease !important;
}

.stButton button:not([kind="primary"]):hover {
    background-color: #DCEEFF !important;
    border-color: #8DBFD9 !important;
    color: #1E3A4B !important;
    transform: translateY(-1px) !important;
}

/* Download Button - Soft Warm Yellow Accent */
.stDownloadButton button {
    background: linear-gradient(135deg, #F6D97A 0%, #F7E7A8 100%) !important;
    color: #4A3B18 !important;
    border: 1.5px solid #E6CA6A !important;
    border-radius: 14px !important;
    font-weight: 700 !important;
    box-shadow: 0 4px 14px rgba(246, 217, 122, 0.35) !important;
    transition: all 0.2s ease !important;
}

.stDownloadButton button:hover {
    background: #EFCF65 !important;
    border-color: #D8B744 !important;
    color: #382A0E !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 18px rgba(246, 217, 122, 0.45) !important;
}

/* Progress Bar - Soft Blue to Warm Yellow Gradient */
.stProgress > div > div > div > div {
    background: linear-gradient(90deg, #8DBFD9 0%, #F6D97A 100%) !important;
    border-radius: 999px !important;
}

.stProgress > div > div > div {
    background-color: #EADCCF !important;
    border-radius: 999px !important;
}

/* Expander Styling */
div[data-testid="stExpander"] {
    background-color: #FFFDF8 !important;
    border: 1.5px solid #E5DDD3 !important;
    border-radius: 14px !important;
    box-shadow: 0 2px 8px rgba(229, 221, 211, 0.3) !important;
}

/* Checkbox accent */
input[type="checkbox"] {
    accent-color: #8DBFD9 !important;
    width: 1.15rem;
    height: 1.15rem;
    cursor: pointer;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

PRIORITIES = {"High": 0, "Medium": 1, "Low": 2}
SUPPORTED_MODELS = [
    "openai/gpt-oss-120b",
    "openai/gpt-oss-20b",
    "qwen/qwen3.8-27b",
    "allam-2-7b",
]

# Session state initialization
if "tasks" not in st.session_state:
    st.session_state.tasks = []
if "notes_input" not in st.session_state:
    st.session_state.notes_input = ""
if "raw_llm_json" not in st.session_state:
    st.session_state.raw_llm_json = None


def mask_key(key: str) -> str:
    """Safely format API key for display without exposing secrets."""
    if not key:
        return "None"
    if len(key) <= 8:
        return "****"
    return f"{key[:6]}...{key[-4:]}"


def call_groq_api(notes: str, api_key: str, model: str, today: date) -> list[dict]:
    """
    Call Groq LLM to convert unstructured notes into a structured list of tasks.
    Robustly handles all HTTP errors (400, 401, 403, 404, 429, 500) and timeouts.
    """
    today_str = today.isoformat()
    day_name = today.strftime("%A")

    system_prompt = (
        "You are an expert AI task extractor for a personal productivity to-do list.\n"
        f"Today's date is {today_str} ({day_name}).\n\n"
        "Instructions:\n"
        "1. Extract distinct, actionable tasks from the user's messy notes.\n"
        "2. For each task, assign priority strictly as 'High', 'Medium', or 'Low':\n"
        "   - 'High': Urgent, critical, time-sensitive (e.g. today/tomorrow, explicit urgency, crucial deadlines).\n"
        "   - 'Medium': Routine important tasks with reasonable timeframes.\n"
        "   - 'Low': Optional, non-urgent, someday chores, or casual reminders.\n"
        "3. Interpret relative deadlines accurately based on the current date provided:\n"
        f"   - 'today' -> {today_str}\n"
        "   - 'tomorrow', 'this Friday', 'next week', 'by Monday', etc. MUST be calculated as exact YYYY-MM-DD dates relative to today.\n"
        "   - If no specific date or timeframe is mentioned in the note, set deadline strictly to 'Not specified'. NEVER invent or hallucinate dates.\n"
        "4. Return ONLY a valid JSON object matching this exact schema with NO surrounding markdown or conversational text:\n"
        '{"tasks": [{"task": "Task title", "priority": "High" | "Medium" | "Low", "deadline": "YYYY-MM-DD or Not specified"}]}'
    )

    user_prompt = f"Today's date: {today_str} ({day_name})\n\nNotes:\n{notes}"

    content_str = ""

    # Path A: Using official Groq Python SDK
    if GROQ_SDK_AVAILABLE:
        try:
            client = Groq(api_key=api_key, timeout=45.0)
            chat_completion = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                response_format={"type": "json_object"},
                temperature=0.0,
            )
            content_str = chat_completion.choices[0].message.content or ""
        except BadRequestError as err:
            raise RuntimeError(f"Bad Request (HTTP 400): {err.message}. Please check request format or parameters.") from err
        except AuthenticationError as err:
            raise RuntimeError("Authentication Failed (HTTP 401): Invalid Groq API key. Please check your key in the .env file or sidebar.") from err
        except PermissionDeniedError as err:
            raise RuntimeError("Permission Denied (HTTP 403): Your account does not have access to this resource or model.") from err
        except NotFoundError as err:
            raise RuntimeError(f"Resource Not Found (HTTP 404): The model '{model}' was not found on Groq. Please select a supported model such as 'openai/gpt-oss-120b'.") from err
        except RateLimitError as err:
            raise RuntimeError("Rate Limit Exceeded (HTTP 429): You have hit Groq's request or token limits. Please wait a few moments before retrying.") from err
        except InternalServerError as err:
            raise RuntimeError(f"Groq Server Error (HTTP 500/503): Groq servers are currently experiencing issues ({err.message}). Please try again shortly.") from err
        except APIConnectionError as err:
            raise RuntimeError(f"Network Connection Failed: Could not connect to Groq API. Please verify your internet connection. Details: {err}") from err
        except APIStatusError as err:
            raise RuntimeError(f"Groq API Error (HTTP {err.status_code}): {err.message}") from err
        except Exception as err:
            raise RuntimeError(f"Unexpected error when calling Groq SDK: {err}") from err

    # Path B: Fallback using direct requests
    else:
        import requests
        try:
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            }
            body = {
                "model": model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                "response_format": {"type": "json_object"},
                "temperature": 0.0,
            }
            resp = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers,
                json=body,
                timeout=45,
            )

            if resp.status_code == 400:
                raise RuntimeError(f"Bad Request (HTTP 400): {resp.text}")
            elif resp.status_code == 401:
                raise RuntimeError("Authentication Failed (HTTP 401): Invalid Groq API key. Check .env file.")
            elif resp.status_code == 403:
                raise RuntimeError("Permission Denied (HTTP 403): Groq account does not have permission.")
            elif resp.status_code == 404:
                raise RuntimeError(f"Model Not Found (HTTP 404): Model '{model}' not found on Groq.")
            elif resp.status_code == 429:
                raise RuntimeError("Rate Limit Reached (HTTP 429): Groq API rate limit exceeded. Please wait.")
            elif resp.status_code >= 500:
                raise RuntimeError(f"Groq Server Error (HTTP {resp.status_code}): {resp.text}")
            
            resp.raise_for_status()
            data = resp.json()
            content_str = data["choices"][0]["message"]["content"]
        except requests.Timeout as err:
            raise RuntimeError("API Timeout: Groq did not respond within 45 seconds. Please try again.") from err
        except requests.ConnectionError as err:
            raise RuntimeError("Network Connection Failed: Unable to reach api.groq.com. Check your network.") from err
        except requests.RequestException as err:
            raise RuntimeError(f"HTTP Request failed: {err}") from err

    # Parse and validate JSON structure
    try:
        parsed_json = json.loads(content_str)
    except json.JSONDecodeError as err:
        raise ValueError(f"LLM returned invalid JSON. Raw output: {content_str[:200]}") from err

    st.session_state.raw_llm_json = parsed_json

    raw_tasks = parsed_json.get("tasks", [])
    if not isinstance(raw_tasks, list):
        raise ValueError("LLM response did not contain a valid 'tasks' list.")

    extracted = []
    for idx, item in enumerate(raw_tasks):
        if not isinstance(item, dict):
            continue
        task_name = str(item.get("task", "")).strip()
        if not task_name:
            continue

        raw_priority = str(item.get("priority", "Medium")).strip().title()
        priority = raw_priority if raw_priority in PRIORITIES else "Medium"
        deadline = str(item.get("deadline", "Not specified")).strip() or "Not specified"

        extracted.append({
            "id": f"task_{idx}_{today_str}",
            "task": task_name,
            "priority": priority,
            "deadline": deadline,
            "completed": False,
        })

    # Sort tasks by priority (High -> Medium -> Low)
    return sorted(extracted, key=lambda x: PRIORITIES[x["priority"]])


# Sidebar: Configuration & Details
with st.sidebar:
    st.markdown("### ⚙️ Settings & API")
    
    # API Key Handling
    env_api_key = os.getenv("GROQ_API_KEY", "").strip()
    user_api_key = st.text_input(
        "Groq API Key",
        value=env_api_key,
        type="password",
        help="Reads automatically from .env or you can enter one directly here.",
    )
    active_api_key = user_api_key.strip() if user_api_key else env_api_key

    if active_api_key:
        st.success(f"● Connected ({mask_key(active_api_key)})", icon="🔑")
    else:
        st.error("Missing Groq API Key! Please enter one above or set in .env", icon="⚠️")

    # Model Selection
    selected_model = st.selectbox(
        "Active Model",
        options=SUPPORTED_MODELS,
        index=0,
        help="openai/gpt-oss-120b is the primary recommended high-capacity model.",
    )

    st.markdown("---")
    st.markdown("### 📌 Project Metadata")
    st.write("**Course:** GenAI Mini Project")
    st.write("**Problem Statement:** 46")
    st.write("**Roll No.:** 46")
    st.write(f"**SDK Engine:** `{'groq-python' if GROQ_SDK_AVAILABLE else 'requests'}`")
    st.write(f"**Date:** `{date.today().isoformat()} ({date.today().strftime('%A')})`")
    
    st.markdown("---")
    st.caption("💡 Key is loaded securely from `.env`. Never exposed in UI or code.")


# Main App Banner - Pastel Blue, Beige & Warm Yellow
st.markdown(
    f"""
    <div class="main-header">
        <div class="main-title">
            <span>✨</span> TaskWise AI
        </div>
        <div class="sub-title">
            Transform messy, unstructured notes into a beautifully organized, prioritized to-do list with smart deadline calculation.
        </div>
        <div class="badge-row">
            <span class="pill-badge pill-roll">🎓 College Mini Project · Roll No. 46</span>
            <span class="pill-badge pill-model">⚡ Model: {selected_model}</span>
            <span class="pill-badge pill-date">📅 Today: {date.today().strftime('%B %d, %Y')} ({date.today().strftime('%A')})</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Sample Presets for Quick Testing
SAMPLE_PRESETS = {
    "📚 College Assignment Sprint": (
        "Finish physics assignment by tomorrow. Submit GenAI mini project on Monday. "
        "Call mom tonight. Buy new notebooks sometime this week. "
        "Meeting with project guide at 4pm on Wednesday."
    ),
    "💼 Project & Dev Tasks": (
        "Urgent: Fix authentication token bug today before the release. "
        "Write documentation for all REST API endpoints by Friday. "
        "Review PR #12 tomorrow morning. Plan Q1 roadmap next month."
    ),
    "🛒 Household & Errands": (
        "Buy groceries: oats, almond milk, and apples. Clean the study room whenever free. "
        "Pay electricity bill urgently today! Renew gym membership by next week."
    ),
}

st.markdown("#### 📝 Input Your Messy Notes")

# Quick fill sample buttons
preset_cols = st.columns(len(SAMPLE_PRESETS))
for col, (label, sample_text) in zip(preset_cols, SAMPLE_PRESETS.items()):
    with col:
        if st.button(label, use_container_width=True):
            st.session_state.notes_input = sample_text

notes_text = st.text_area(
    label="Paste whatever is on your mind — reminders, dates, fragments, emails:",
    value=st.session_state.notes_input,
    height=140,
    placeholder="E.g., Call professor tomorrow morning, finish report by Friday, buy groceries sometime...",
    key="notes_textarea",
)

# Action Buttons
btn_col1, btn_col2, btn_col3 = st.columns([2, 1, 1])

with btn_col1:
    generate_clicked = st.button("✨ Generate Prioritised To-Do List", type="primary", use_container_width=True)

with btn_col2:
    if st.button("🗑️ Clear All", use_container_width=True):
        st.session_state.tasks = []
        st.session_state.raw_llm_json = None
        st.session_state.notes_input = ""
        st.rerun()

with btn_col3:
    if st.session_state.tasks:
        # Mark all toggle
        all_completed = all(t.get("completed", False) for t in st.session_state.tasks)
        btn_label = "↩️ Uncheck All" if all_completed else "✅ Complete All"
        if st.button(btn_label, use_container_width=True):
            new_status = not all_completed
            for t in st.session_state.tasks:
                t["completed"] = new_status
            st.rerun()


# Trigger Task Generation
if generate_clicked:
    clean_notes = notes_text.strip()
    if not clean_notes:
        st.warning("⚠️ Please enter some messy notes or click a sample preset above before generating.")
    elif not active_api_key:
        st.error("🔑 Please provide a valid Groq API key in the sidebar or local .env file.")
    else:
        with st.spinner("🤖 Consulting Groq AI to extract and prioritize your tasks..."):
            try:
                extracted_tasks = call_groq_api(
                    notes=clean_notes,
                    api_key=active_api_key,
                    model=selected_model,
                    today=date.today(),
                )
                st.session_state.tasks = extracted_tasks
                if not extracted_tasks:
                    st.info("ℹ️ No actionable tasks found in your notes. Try adding explicit actions or chores.")
                else:
                    st.toast(f"✨ Successfully generated {len(extracted_tasks)} tasks!", icon="🎉")
            except Exception as e:
                st.error(f"❌ Error: {e}")


# Display Generated Tasks
if st.session_state.tasks:
    st.markdown("---")
    st.markdown("### 📋 Your Prioritised To-Do List")

    total_tasks = len(st.session_state.tasks)
    completed_count = sum(1 for t in st.session_state.tasks if t.get("completed", False))
    pending_count = total_tasks - completed_count
    high_count = sum(1 for t in st.session_state.tasks if t.get("priority") == "High")
    med_count = sum(1 for t in st.session_state.tasks if t.get("priority") == "Medium")
    low_count = sum(1 for t in st.session_state.tasks if t.get("priority") == "Low")

    # Pretty Dashboard Metric Cards
    st.markdown(
        f"""
        <div class="stats-container">
            <div class="stat-card">
                <div class="stat-val">{total_tasks}</div>
                <div class="stat-lbl">Total Tasks</div>
            </div>
            <div class="stat-card">
                <div class="stat-val" style="color: #1E6B3E;">{completed_count}</div>
                <div class="stat-lbl">Completed</div>
            </div>
            <div class="stat-card">
                <div class="stat-val" style="color: #9A6700;">{pending_count}</div>
                <div class="stat-lbl">Pending</div>
            </div>
            <div class="stat-card">
                <div class="stat-val" style="color: #C53047;">{high_count}</div>
                <div class="stat-lbl">High Priority</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Progress Bar
    progress_val = completed_count / total_tasks if total_tasks > 0 else 0.0
    st.progress(
        progress_val,
        text=f"Progress: {completed_count} of {total_tasks} completed ({int(progress_val * 100)}%)",
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # Render Task Cards with Interactive Checkboxes
    for i, item in enumerate(st.session_state.tasks):
        is_done = item.get("completed", False)
        priority = item.get("priority", "Medium")
        deadline = item.get("deadline", "Not specified")

        # Determine priority styling
        if priority == "High":
            priority_html = '<span class="badge-priority-high">🔴 High</span>'
        elif priority == "Medium":
            priority_html = '<span class="badge-priority-med">🟡 Medium</span>'
        else:
            priority_html = '<span class="badge-priority-low">🟢 Low</span>'

        deadline_html = f'<span class="badge-deadline">📅 {deadline}</span>'

        card_class = "task-card task-completed" if is_done else "task-card"

        col_chk, col_content = st.columns([0.06, 0.94])
        
        with col_chk:
            # Checkbox key must remain stable across reruns
            chk_key = f"chk_{i}_{item['id']}"
            checked = st.checkbox(
                label=f"Done {i}",
                value=is_done,
                key=chk_key,
                label_visibility="collapsed",
            )
            if checked != is_done:
                st.session_state.tasks[i]["completed"] = checked
                st.rerun()

        with col_content:
            st.markdown(
                f"""
                <div class="{card_class}">
                    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
                        <span class="task-text">{item['task']}</span>
                        <div style="display: flex; gap: 8px; align-items: center;">
                            {priority_html}
                            {deadline_html}
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)

    # Export & Inspection Actions
    exp_col1, exp_col2 = st.columns([1, 1])
    
    with exp_col1:
        # Prepare CSV Export DataFrame
        export_data = [
            {
                "Task": t["task"],
                "Priority": t["priority"],
                "Deadline": t["deadline"],
                "Status": "Completed" if t.get("completed", False) else "Pending",
                "Created Date": date.today().isoformat(),
            }
            for t in st.session_state.tasks
        ]
        df_export = pd.DataFrame(export_data)
        csv_bytes = df_export.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="⬇️ Download To-Do List (CSV)",
            data=csv_bytes,
            file_name=f"taskwise_todo_{date.today().isoformat()}.csv",
            mime="text/csv",
            use_container_width=True,
        )

    with exp_col2:
        with st.expander("🔍 View Structured LLM JSON"):
            if st.session_state.raw_llm_json:
                st.json(st.session_state.raw_llm_json)
            else:
                st.json({"tasks": st.session_state.tasks})
