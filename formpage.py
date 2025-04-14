import streamlit as st
import pandas as pd
import re
from importrequests import *

# Set the page configuration
st.set_page_config(
    page_title="LWR - Document Submission - TEST",  # Tab title
    page_icon=":page_facing_up:",
)

# Load logo
st.image("logo.jpg", width=300)

st.title("LWR – Document Submission Request")



# Apply CSS for minimalist design
st.markdown("""
    <style>
    .main {
        background-color: #f5f5f5;
        padding: 20px;
        border-radius: 10px;
    }
    .stButton button {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 10px 20px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# Main container
with st.container():
    
    st.subheader("1) Email*")
    email = st.text_input("Submitter's Email Address:")

    # Table 1   
    st.subheader("2) MIDP Check*")
    url = r"https://app.powerbi.com/groups/me/apps/64f8028b-7510-4069-8b8d-f3ba70f53d38/reports/e095f418-8cfd-4504-b8d6-54d3cf7ea9af/c47fc146c7a267925009?ctid=a2bed0c4-5957-4f73-b0c2-a811407590fb&experience=power-bi&bookmarkGuid=b12e777100e1567d8ccc"
    midp_confirmation = st.radio(
        "Please confirm the documents to be issued are included in the [MIDP](%s):" % url,
        ("Confirmed"),
        index=None
    )

    # Table 2
    st.subheader("3) Submission Title*")
    submission_title = st.text_input("Please provide the Submission Title:")

    # Table 3
    st.subheader("4) Document Container Set on PW (URN)*")
    document_container_set = st.text_input("Please provide a link to the Document of Document Set on Projectwise (URN):")

    # Table 9
    st.subheader("5) Reason for Issue*")
    reason_for_issue = st.radio("What is the Reason for Issue:", ("S2 (For information) - Used to begin co-authoring DCO submission documents", "S5 – (For Client Review & Acceptance)"),
    index=1
    )

    # Table 10
    st.subheader("6) Additional Notes")
    additional_notes = st.text_area("Please provide any Additional Notes for Document Control:")

    # Initialize session state for the table
    if 'table_data' not in st.session_state:
        st.session_state.table_data = [{"Email": "LWRInformationManagement@mottmac.com"}]

    # Function to add a new row
    def add_row():
        st.session_state.table_data.append({"Email": ""})

    # Display the table
    st.subheader("7) Distribution List*")
    st.write("Add email addresses to be notified upon submission:")

    # Create a DataFrame from the session state data
    df = pd.DataFrame(st.session_state.table_data)

    # Display the table with editable cells
    edited_df = st.data_editor(df, hide_index=True)

    # Update the session state with the edited data
    st.session_state.table_data = edited_df.to_dict('records')
        # Add a button to add new rows
    if st.button("Add Row"):
        add_row()


# Submit button
if st.button("Submit"):
    errors = []

    # Ensure all required fields are filled
    if not email:
        errors.append("Email is required.")
    else:
        # Validate email addresses
        email_pattern = re.compile(r"[^@]+@[^@]+\.[^@]+")
        if not email_pattern.match(email):
            errors.append(f"Invalid email address: {email}")
    if not midp_confirmation:
        errors.append("MIDP check is required.")
    if not submission_title:
        errors.append("Submission Title is required.")
    if not document_container_set:
        errors.append("Document Container Set on PW (URN) is required.")
    else:
        # Validate URL
        url_pattern = re.compile(r"https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+")
        if not url_pattern.match(document_container_set):
            errors.append("Document Container Set on PW (URN) must be a valid URL.")
    if not reason_for_issue:
        errors.append("Reason for Issue is required.")
    if not st.session_state.table_data:
        errors.append("At least one email address is required in the Distribution List.")

    # Validate email addresses
    email_pattern = re.compile(r"[^@]+@[^@]+\.[^@]+")
    for row in st.session_state.table_data:
        if not email_pattern.match(row["Email"]) and row['Email'] != '':
            errors.append(f"Invalid email address: {row['Email']}")



    if errors:
        for error in errors:
            st.error(error)
    else:
        # Collect all data into a dictionary
        form_data = {
            "Submitters Email": email,
            "MIDP Confirmation": midp_confirmation,
            "Submission Title": submission_title,
            "Document Container Set on PW (URN)": document_container_set,
            "Reason for Issue": reason_for_issue,
            "Additional Notes": additional_notes,
            "Distribution List": [row["Email"] for row in st.session_state.table_data]
        }
        
        
        submitform(form_data)
        st.success("Form submitted successfully!")

        # Clear all fields
        st.session_state.email = ""
        st.session_state.midp_confirmation = None
        st.session_state.submission_title = ""
        st.session_state.document_container_set = ""
        st.session_state.reason_for_issue = "S2 (For information) - Used to begin co-authoring DCO submission documents"
        st.session_state.additional_notes = ""
        st.session_state.table_data = [{"Email": "LWRInformationManagement@mottmac.com"}]
