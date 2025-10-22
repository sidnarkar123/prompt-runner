import streamlit as st
import json
import uuid
import os
import pandas as pd
import requests
import time

from components.ui import prompt_input, log_viewer, action_buttons
from utils.io_helpers import save_prompt, save_spec, load_prompts, load_logs
from agents.design_agent import prompt_to_spec
from utils import mcp_store

st.set_page_config(page_title="Prompt Runner", layout="wide")
st.title("📝 Streamlit Prompt Runner")

# --- Prompt Input ---
user_prompt = prompt_input()
json_spec = None
case_id = None

if st.button("Submit", key="submit_main"):
    if user_prompt:
        spec_data = prompt_to_spec(user_prompt)
        spec_filename = save_spec(spec_data)
        save_prompt(user_prompt, spec_filename)
        st.success("Prompt processed successfully!")
    else:
        st.error("Please enter a prompt.")

# --- Display Latest JSON Spec ---
if os.path.exists("specs") and user_prompt:
    last_spec_files = sorted(os.listdir("specs"), reverse=True)
    if last_spec_files:
        spec_file = os.path.join("specs", last_spec_files[0])
        with open(spec_file) as f:
            json_spec = json.load(f)
        st.markdown("### Generated JSON Specification")
        st.json(json_spec)
        case_id = os.path.splitext(last_spec_files[0])[0]

# --- Feedback Section (Updated for MCP API) ---
if json_spec and case_id:
    st.markdown("### Feedback")
    col1, col2 = st.columns(2)
    feedback_api = "http://127.0.0.1:5001/api/mcp/feedback"
    if col1.button("👍 Good result"):
        feedback_input = {
            "case_id": case_id,
            "feedback": "up"
        }
        r = requests.post(feedback_api, json=feedback_input)
        st.success(f"Feedback saved! Reward +2 | {r.json()}")
    if col2.button("👎 Needs improvement"):
        feedback_input = {
            "case_id": case_id,
            "feedback": "down"
        }
        r = requests.post(feedback_api, json=feedback_input)
        st.error(f"Feedback saved! Reward -2 | {r.json()}")

# --- Divider ---
st.markdown("---")
st.markdown("### History")

logs = load_logs()
prompt_logs = logs.get("prompt_logs", [])
action_logs = logs.get("action_logs", [])

with st.container():
    col_left, col_right = st.columns([1, 1], gap="large")

    # Prompt Logs
    with col_left:
        st.markdown("**Prompt Logs**")
        if prompt_logs:
            df = pd.DataFrame(prompt_logs)
            df["prompt_preview"] = df["prompt"].apply(lambda s: s[:100]+"…" if len(s)>100 else s)
            display_df = df[["id","timestamp","prompt_preview","spec_filename"]].sort_values("timestamp", ascending=False)
            st.dataframe(display_df, height=260)
        else:
            st.info("No prompt logs available.")

    # Action Logs
    with col_right:
        st.markdown("**Action Logs**")
        if action_logs:
            adf = pd.DataFrame(action_logs)
            adf["details_summary"] = adf["details"].apply(lambda d: ", ".join(f"{k}:{v}" for k,v in d.items()) if d else "")
            display_adf = adf[["timestamp","action","spec_id","details_summary"]].sort_values("timestamp", ascending=False)
            st.dataframe(display_adf, height=260)
        else:
            st.info("No action logs available.")

# --- Sidebar Log Viewer ---
st.sidebar.header("Log Viewer")
past_prompts = load_prompts()
selected_prompt = log_viewer(past_prompts)

if selected_prompt:
    spec_file = os.path.join("specs", f"{selected_prompt}.json")
    if os.path.exists(spec_file):
        with open(spec_file) as f:
            spec_data = json.load(f)
        with st.sidebar.expander("📄 View JSON Spec"):
            st.json(spec_data)
    else:
        st.sidebar.warning("Spec file not found for this prompt.")

# --- Action Buttons in Sidebar ---
action_buttons(selected_prompt)
