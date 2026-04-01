# webui/app.py

import streamlit as st
import requests

API_BASE = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="IAM Automation Portal",
    page_icon="🛂",
    layout="wide"
)

st.title("🛂 IAM Automation Portal")
st.write("Welcome to the IAM Automation Platform Web UI.")
st.write("Use the sidebar to navigate through provisioning tools.")
