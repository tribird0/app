import streamlit as st
import zxcvbn  # A password strength estimation library

# Function to analyze password strength
def analyze_password(password):
    result = zxcvbn.zxcvbn(password)
    return result

# Streamlit app
st.title("Password Strength Analyzer")
st.write("This tool analyzes the strength of your password without storing or transmitting it.")

password = st.text_input("Enter a password to analyze:", type="password")

if password:
    analysis = analyze_password(password)
    st.write(f"Password Strength Score: {analysis['score']}/4")
    st.write(f"Estimated Cracking Time: {analysis['crack_times_display']['offline_slow_hashing_1e4_per_second']}")
    st.write("Feedback:")
    for warning in analysis['feedback']['warning']:
        st.write(f"- {warning}")
    for suggestion in analysis['feedback']['suggestions']:
        st.write(f"- {suggestion}")
