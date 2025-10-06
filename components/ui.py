# ...existing code...
import os
import shutil
import streamlit as st
from utils.io_helpers import log_action, SEND_EVAL_DIR, SEND_UNREAL_DIR, load_logs  # added load_logs import
# ...existing code...

def prompt_input():
    """
    Render a single prompt input widget (no Submit button here to avoid duplicate IDs).
    Returns the entered prompt string (or empty string).
    """
    return st.text_input("Enter your prompt:", key="prompt_input")

def display_json(json_data):
    """Display JSON in the main area."""
    st.json(json_data)

def log_viewer(logs):
    """
    Sidebar selector for past prompts.
    Displays a simple activity card below the selector when a prompt is chosen.
    Returns the selected prompt id or None.
    """
    if not logs:
        st.sidebar.write("No prompts found.")
        return None

    # Selectable list of prompt ids (labels handled elsewhere if present)
    selected = st.sidebar.selectbox("Select a past prompt", options=logs, key="log_selectbox")
    if not selected:
        return None

    st.sidebar.write("Selected Prompt ID:", selected)

    # Activity card: show recent actions that reference this prompt id
    all_logs = load_logs()
    actions = all_logs.get("action_logs", []) if isinstance(all_logs, dict) else []
    # most recent first, filter by spec_id
    related = [a for a in reversed(actions) if a.get("spec_id") == selected]

    # Render a compact card below the selector
    card_html = "<div style='background:#f3f4f6;padding:10px;border-radius:8px;margin-top:8px;'>"
    card_html += "<strong style='font-size:13px;color:#111827'>Recent Activities</strong>"
    if not related:
        card_html += "<div style='color:#6b7280;margin-top:6px;font-size:13px'>No actions recorded for this prompt.</div>"
    else:
        card_html += "<ul style='padding-left:18px;margin-top:6px;color:#111827'>"
        for act in related[:6]:  # show up to 6 recent actions
            ts = act.get("timestamp", "")[:19].replace("T", " ")
            action = act.get("action", "action")
            details = act.get("details") or {}
            # simple detail summary if present
            detail_text = ""
            if isinstance(details, dict) and details:
                # show first key:value pair succinctly
                k = next(iter(details))
                detail_text = f" — {k}: {details.get(k)}"
            card_html += f"<li style='margin-bottom:6px;font-size:13px'>{ts} — <span style='color:#0b2447;font-weight:600'>{action}</span>{detail_text}</li>"
        card_html += "</ul>"
    card_html += "</div>"

    st.sidebar.markdown(card_html, unsafe_allow_html=True)

    return selected

def action_buttons(selected_prompt):
    """
    Sidebar action buttons to route the selected spec.
    Copies the spec file into the destination folder and logs the action.
    """
    if not selected_prompt:
        st.sidebar.info("Select a prompt to enable routing actions.")
        return

    spec_path = os.path.join("specs", f"{selected_prompt}.json")
    if not os.path.exists(spec_path):
        st.sidebar.error("Spec file not found for the selected prompt.")
        return

    # Unique keys include the prompt id to avoid duplicate-element errors
    if st.sidebar.button("Send to Evaluator", key=f"send_eval_{selected_prompt}"):
        os.makedirs(SEND_EVAL_DIR, exist_ok=True)
        dest = os.path.join(SEND_EVAL_DIR, os.path.basename(spec_path))
        try:
            shutil.copyfile(spec_path, dest)
            log_action("send_to_evaluator", selected_prompt)
            st.sidebar.success("Spec sent to Evaluator.")
        except Exception as e:
            st.sidebar.error(f"Failed to send to Evaluator: {e}")

    if st.sidebar.button("Send to Unreal Engine", key=f"send_unreal_{selected_prompt}"):
        os.makedirs(SEND_UNREAL_DIR, exist_ok=True)
        dest = os.path.join(SEND_UNREAL_DIR, os.path.basename(spec_path))
        try:
            shutil.copyfile(spec_path, dest)
            log_action("send_to_unreal", selected_prompt)
            st.sidebar.success("Spec sent to Unreal Engine.")
        except Exception as e:
            st.sidebar.error(f"Failed to send to Unreal Engine: {e}")
# ...existing code...
