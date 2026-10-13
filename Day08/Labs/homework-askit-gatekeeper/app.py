import streamlit as st

from gatekeeper import needs_approval, route, safe_to_remember


st.set_page_config(page_title="Gatekeeper", page_icon="🛡️")
st.title("Gatekeeper Demo")
st.write("Enter text and run the gatekeeper checks.")

text = st.text_area("Text", height=120, placeholder="Type a request or note here")

col1, col2, col3 = st.columns(3)

with col1:
    route_clicked = st.button("Route")
with col2:
    approval_clicked = st.button("Needs approval")
with col3:
    remember_clicked = st.button("Safe to remember")

if route_clicked:
    try:
        st.subheader("Route result")
        st.write(route(text))
    except Exception as exc:
        st.error(str(exc))

if approval_clicked:
    try:
        st.subheader("Approval result")
        action = st.selectbox("Action", ["search_kb", "get_ticket", "reset_password", "update_ticket", "grant_access"])
        user_id = st.text_input("User ID", value="EMP-2000")
        hour = st.number_input("Hour", min_value=0, max_value=23, value=12, step=1)
        result = needs_approval(action, user_id, int(hour))
        st.json(result)
    except Exception as exc:
        st.error(str(exc))

if remember_clicked:
    st.subheader("Memory result")
    st.write(safe_to_remember(text))
