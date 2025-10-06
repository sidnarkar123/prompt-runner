import streamlit as st
import json
import os
import pandas as pd
from components.ui import prompt_input, log_viewer, action_buttons
from utils.io_helpers import save_prompt, save_spec, load_prompts, load_logs
from agents.design_agent import prompt_to_spec

# Set up the Streamlit app title and layout
st.title("Streamlit Prompt Runner")

# --- Prompt Input Section ---
user_prompt = prompt_input()

# --- JSON Output Placeholder ---
json_spec = None

# When Submit button is clicked
if st.button("Submit", key="submit_main"):
    if user_prompt:
        # Save the user prompt
        save_prompt(user_prompt)

        # Generate JSON specification using the Design Agent
        json_spec = prompt_to_spec(user_prompt)

        # Save the generated JSON spec
        save_spec(json_spec)

        st.success("Prompt processed successfully!")
    else:
        st.error("Please enter a prompt.")

# --- Display JSON Output ABOVE History ---
if json_spec:
    st.markdown("### Generated JSON Specification")
    st.json(json_spec)

# --- Divider before history ---
st.markdown("---")

# --- 📜 HISTORY SECTION (below JSON output) ---
st.markdown("### History")

# Load logs safely
logs = load_logs()
prompt_logs = logs.get("prompt_logs", []) if isinstance(logs, dict) else []
action_logs = logs.get("action_logs", []) if isinstance(logs, dict) else []

with st.container():
    col_left, col_right = st.columns([1, 1], gap="large")

    # --- LEFT: Prompt Logs ---
    with col_left:
        st.markdown("<div class='card'><strong>Prompt Logs</strong></div>", unsafe_allow_html=True)
        if prompt_logs:
            df = pd.DataFrame(prompt_logs)
            if "prompt" not in df.columns:
                df["prompt"] = ""
            df["prompt_preview"] = df["prompt"].apply(
                lambda s: (s[:100] + "…") if isinstance(s, str) and len(s) > 100 else s
            )
            display_df = df[["id", "timestamp", "prompt_preview", "spec_filename"]].copy()
            display_df = display_df.sort_values("timestamp", ascending=False).reset_index(drop=True)
            st.dataframe(display_df, height=260)
        else:
            st.info("No prompt logs available.")

    # --- RIGHT: Action Logs ---
    with col_right:
        st.markdown("<div class='card'><strong>Action Logs</strong></div>", unsafe_allow_html=True)
        if action_logs:
            adf = pd.DataFrame(action_logs)
            if "details" not in adf.columns:
                adf["details"] = [{} for _ in range(len(adf))]
            adf["details_summary"] = adf["details"].apply(
                lambda d: ", ".join(f"{k}: {v}" for k, v in d.items()) if isinstance(d, dict) and d else ""
            )
            display_adf = adf[["timestamp", "action", "spec_id", "details_summary"]].copy()
            display_adf = display_adf.sort_values("timestamp", ascending=False).reset_index(drop=True)
            st.dataframe(display_adf, height=260)
        else:
            st.info("No action logs available.")

# --- Sidebar Log Viewer Section ---
st.sidebar.header("Log Viewer")
past_prompts = load_prompts()
selected_prompt = log_viewer(past_prompts)

# --- Show JSON Spec of Selected Prompt INSIDE SIDEBAR ---
if selected_prompt:
    spec_file = os.path.join("specs", f"{selected_prompt}.json")
    if os.path.exists(spec_file):
        with open(spec_file) as f:
            spec_data = json.load(f)
        with st.sidebar.expander("📄 View JSON Spec"):
            st.json(spec_data)
    else:
        st.sidebar.warning("Spec file not found for this prompt.")

# --- Action Routing Section (still in sidebar) ---
action_buttons(selected_prompt)
