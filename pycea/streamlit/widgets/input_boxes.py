import streamlit as st


PRESSURE_UNITS = {"bar":1e5, "Pa":1, "psi":6895, "MPa":1e6}

def pressure_input(container: st, key: str, name: str = "Pressure input"):

    step_key = key+"_STEP"
    format_key = key+"_FORMAT"
    key_value = key+"_VALUE"
    key_unit = key+"_UNIT"
    key_widget = key+"_WIDGET"

    if key not in st.session_state:
        st.session_state[key_widget] = {}

    if step_key not in st.session_state[key_widget]:
        st.session_state[key_widget][step_key] = 1.0

    if format_key not in st.session_state[key_widget]:
        st.session_state[key_widget][format_key] = "%.1f"

    if key not in st.session_state:
        st.session_state[key] = 101325.0

    if key_unit not in st.session_state[key_widget]:
        st.session_state[key_widget][key_unit] = "bar"

    if key_value not in st.session_state[key_widget]:
        st.session_state[key_widget][key_value] = st.session_state[key]/1e5


    def on_change_unit():
        st.session_state[key_widget][key_unit] = st.session_state[key_unit]
        if st.session_state[key_widget][key_unit] == "MPa":
            st.session_state[key_widget][step_key] = 0.1
            st.session_state[key_widget][format_key] = "%.2f"

        if st.session_state[key_widget][key_unit] == "psi":
            st.session_state[key_widget][step_key] = 1.0
            st.session_state[key_widget][format_key] = "%.1f"

        if st.session_state[key_widget][key_unit] == "Pa":
            st.session_state[key_widget][step_key] = 100.0
            st.session_state[key_widget][format_key] = "%.0f"

        if st.session_state[key_widget][key_unit] == "bar":
            st.session_state[key_widget][step_key] = 1.0
            st.session_state[key_widget][format_key] = "%.1f"

        st.session_state[key_widget][key_value] = st.session_state[key] / PRESSURE_UNITS[st.session_state[key_widget][key_unit]]
        st.session_state[key_value] = st.session_state[key_widget][key_value]
    
    def on_change_pressure():
        st.session_state[key_widget][key_value] = st.session_state[key_value]
        st.session_state[key] = st.session_state[key_widget][key_value] * PRESSURE_UNITS[st.session_state[key_widget][key_unit]]

    col1, col2 = container.columns([2,1], vertical_alignment="bottom")
    col1.number_input(name, step=st.session_state[key_widget][step_key], format=st.session_state[key_widget][format_key], key=key_value, on_change=on_change_pressure, value=st.session_state[key_widget][key_value])
    col2.selectbox("Unit", PRESSURE_UNITS, key=key_unit, on_change=on_change_unit)