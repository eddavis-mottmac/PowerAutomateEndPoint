import streamlit as st
import pandas as pd
import re
from importrequests import *


midp_url = st.secrets["endpoint"]["midp_url"]



# Set the page configuration
st.set_page_config(
    page_title="LWR - Document Submission",  # Tab title
    page_icon=":page_facing_up:",
    layout="wide",
)


# Load logo
st.image("logo.jpg", width=300)

st.title("LWR – Document Submission Request")
st.write("*The OCRA accronym used throughout this form stands for Originator/Checker/Reviewer/Approver")

# Main container
with st.container():
    
    st.subheader("1) Email*")
    if 'email' not in st.session_state:
        st.session_state.email = ''
    email = st.text_input("Submitter's Email Address:", value=st.session_state.email)

    # Table 9
    st.subheader("2) Project Contract*")
    if 'contract' not in st.session_state:
        st.session_state.contract = "TEDD - Teddington"
    contract = st.radio("Please choose one option for the whole package:", ("TEDD - Teddington", "BECK - Bectkon"),
    index=0
    )

    # Table 2
    st.subheader("3) Transmittal Title*")
    if 'submission_title' not in st.session_state:
        st.session_state.submission_title = ''
    submission_title = st.text_input("Please provide the Transmittal Title:", value=st.session_state.submission_title)

    # Table 9
    st.subheader("4) Reason for Issue*")
    if 'reason_for_issue' not in st.session_state:
        st.session_state.reason_for_issue = "S2 (For information) - Document will not be reviewed by client"
    reason_for_issue = st.radio("Please choose one option for the whole package. If you need to include supporting files for information, you will be able to specify this later in the form:", ("S2 (For information) - Document will not be formally reviewed by client", "S5 – (For Client Review & Acceptance)"),
    index=1
    )

    
    # Ask the initial question
    st.subheader("5) Documents for Issue*")
    CDE = st.radio("Documents can only be issued from ProjectWise. Please choose one of the following options:", ("List each document individually below", "Submit a link to a ProjectWise list"))

    # Display the next question based on the previous response
    if CDE == "List each document individually below":
        # Display the table
        st.write("Please add the details of the documents you are submitting:")
        doc_df = pd.DataFrame(
            [
            {'Document Number': 'J698-JMM-XXXX-XXXX-XX-XX-000000', 'Document Title': 'Example Document - Please Replace line', 'Link to Native File': 'https://www.example.com/', 'Digital OCRA* Recorded': False, 'Link to PDF (Use Native File Link if N/A)': 'https://www.example.com/'}
        ]
        )
        doc_edited_df = st.data_editor(doc_df, num_rows="dynamic", column_config={
            "Link to Native File": st.column_config.LinkColumn(
                "Link to Native File",
                help="Link to the native file e.g. the word document file. This must have completed digital OCRA*",
                validate=r"^https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+",
                max_chars=255,
                display_text=r"https://(.*?)\.streamlit\.app"
            ),
            "Link to PDF (Use Native File Link if N/A)": st.column_config.LinkColumn(
                "Link to PDF (Use Native File Link if N/A)",
                help="Link to a PDF'd version of the native file, this is not required to be undergo OCRA*",
                validate=r"^https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+",
                max_chars=255,
                display_text=r"https://(.*?)\.streamlit\.app"
            ),
            "Document Number": st.column_config.TextColumn(
                "Document Number",
                help="Please enter the document number as listed in the MIDP. Invalid document numbers will not be accepted.",
                validate=r"^J698-JMM-[A-Za-z0-9]{4}-[A-Za-z0-9]{4,8}-[A-Za-z0-9]{2}-[A-Za-z0-9]{2}-\d{6}$"
            )
        })


        # Supporting Documents
        st.write("Include details of supporting documents within your main document, such as PEIR maps within the PEIR or calculations within the appendix of a report. These need to be fully OCRA*'d but will only be issued to the client at S2 (For Information):")
        sup_doc_df = pd.DataFrame(
            [
            {'Document Number': '', 'Document Title': '', 'Link to Native File': '', 'Digital OCRA* Recorded': False, 'Link to PDF (Use Native File Link if N/A)': ''}
        ]
        ).iloc[1:].reset_index(drop=True)
        sup_doc_edited_df = st.data_editor(sup_doc_df, num_rows="dynamic", column_config={
            "Link to Native File": st.column_config.LinkColumn(
                "Link to Native File",
                help="Link to the native file e.g. the word document file. This must have completed digital OCRA*",
                validate=r"^https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+",
                max_chars=255,
                display_text=r"https://(.*?)\.streamlit\.app"
            ),
            "Link to PDF (Use Native File Link if N/A)": st.column_config.LinkColumn(
                "Link to PDF (Use Native File Link if N/A)",
                help="Link to a PDF'd version of the native file for Document Control to submit with the native file. This is not required to be OCRA*'d",
                validate=r"^https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+",
                max_chars=255,
                display_text=r"https://(.*?)\.streamlit\.app"
            ),
            "Document Number": st.column_config.TextColumn(
                "Document Number",
                help="Please enter the document number as listed in the MIDP. Invalid document numbers will not be accepted.",
                validate=r"^J698-JMM-[A-Za-z0-9]{4}-[A-Za-z0-9]{4,8}-[A-Za-z0-9]{2}-[A-Za-z0-9]{2}-\d{6}$"
            )
        }, key="unique_key_1")
    
    else:
        st.write("Please place the documents in a Projectwise List and provide a link:")
        if 'doc_set' not in st.session_state:
            st.session_state.doc_set = ''
        doc_set = st.text_input("Please ensure that all documents within the list have the correct status (Use S5 to trigger Client Review and Comment, and S2 if issuing for information only or if the document is supporting information e.g. A calculation within the appendix of the main report):", value=st.session_state.doc_set, placeholder="https://example.com")


    # Distribution List Table
    # Display the table
    st.subheader("6) Distribution Lists")
    st.write("Add Thames Water email addresses to notified for approval/review of the documents:")

    # Create a DataFrame from the session state data
    dist_rev_df = pd.DataFrame([{"Email": "LWRDocumentControl@jacobs.com", "Role": "For Information"}])
    table_edited_df = st.data_editor(dist_rev_df, num_rows="dynamic", column_config={
        "Role": st.column_config.SelectboxColumn(
            "Role",
            help="Specify if this person should be notified for information only or included as a client reviewer (Thames Water employees only)",
            options = ["For Information", "For Client Review"]
        )
    }, width=750)

    # Table 1   
    st.subheader("7) Please confirm you have completed the necessary Quality Assurance checks*")
    
    # List of checks
    items = [f"All listed document numbers are registered in [MIDP](%s):" % midp_url, 'All listed documents have successfully passed the checker-reviewer-approver workflow in ProjectWise', 'The names listed for OCRA* within all listed documents match those in the digital workflow', 'All listed documents reference the correct revision throughout the document', 'All documents listed have the correct security classification', 'All listed documents (exluding models/drawings) headers contain the correct document number and revision', 'All listed documents (exclusing models/drawings) footers contain the correct document title, security classification and page number']

    
    # Create checkboxes for each item
    selected_items = []
    for item in items:
        if st.checkbox(item):
            selected_items.append(item)

        # Table 10
    st.subheader("8) Transmittal Comments")
    if 'additional_notes' not in st.session_state:
        st.session_state.additional_notes = ''
    additional_notes = st.text_area("Supporting comments to be displayed on Transmittal Cover note or for Document Control information:", value=st.session_state.additional_notes)

# Submit button
if st.button("Submit"):
    errors = []

    # Ensure all required fields are filled
    if not email:
        errors.append("Question 1: Email is required.")
    else:
        # Validate email addresses
        email_pattern = re.compile(r"[^@]+@[^@]+\.[^@]+")
        if not email_pattern.match(email):
            errors.append(f"Question 1: Invalid email address: {email}")
    if not submission_title:
        errors.append("Question 3: Submission Title is required.")
    if not reason_for_issue:
        errors.append("Question 4: Reason for Issue is required.")
    if CDE == "List each document individually below":
        if any(not x for x in doc_edited_df['Digital OCRA* Recorded'].tolist()):
            errors.append("Question 5: All Documents for issue must have Digital OCRA* Completed")
    if len(table_edited_df)==0:
        errors.append("Question 6: At least one email address is required in the Distribution List.")
    if not len(selected_items) == 7:
        errors.append("Question 7: Quality Assurance checks must be completed.")

    # Validate email addresses
    email_pattern = re.compile(r"[^@]+@[^@]+\.[^@]+")
    for index, row in table_edited_df.iterrows():
        dist_emails = row["Email"]
        if not email_pattern.match(dist_emails) and dist_emails != '':
            errors.append(f"Invalid email address: {dist_emails}")

    if errors:
        for error in errors:
            st.error(error)
    else:
        # Collect all data into a dictionary

        if CDE == 'List each document individually below':
            documents = {
                "Documents Numbers": doc_edited_df['Document Number'].tolist(),
                "Documents Titles": doc_edited_df['Document Title'].tolist(),
                "Native Links": doc_edited_df['Link to Native File'].tolist(),
                "PDF Links": doc_edited_df['Link to PDF (Use Native File Link if N/A)'].tolist()
            }

            sup_documents = {
                "Documents Numbers": sup_doc_edited_df['Document Number'].tolist(),
                "Documents Titles": sup_doc_edited_df['Document Title'].tolist(),
                "Native Links": sup_doc_edited_df['Link to Native File'].tolist(),
                "PDF Links": sup_doc_edited_df['Link to PDF (Use Native File Link if N/A)'].tolist()
            }
            doc_set=''
        else:
            documents = {
                "Documents Numbers": [],
                "Documents Titles": [],
                "Native Links": [],
                "PDF Links": []
            }

            sup_documents = {
                "Documents Numbers": [],
                "Documents Titles": [],
                "Native Links": [],
                "PDF Links": []
            }

        Distribution_List = {
            "Emails": table_edited_df['Email'].tolist(),
            "Review/For Information": table_edited_df['Role'].tolist()
        }


        form_data = {
            "Submitters Email": email,
            "Contract": contract.split("-")[0].replace(" ",""),
            "CDE": CDE,
            "Projectwise Link": doc_set,
            "Submission Title": submission_title,
            "Reason for Issue": reason_for_issue,
            "Documents": documents,
            "Supporting Documents": sup_documents,
            "Distribution List Reviewers": Distribution_List,
            "Additional Notes": additional_notes
        }

       
        response = submitform(form_data)
        if response.status_code == 200:
            ("Thank you, you have successfully submitted the form! You shall receieve a confirmation email shortly.")
        else:
            st.error(f"{response.status_code} error code, please contact systems administrator")

        # Clear all fields
        st.session_state.email = ""
        st.session_state.submission_title = ""
        st.session_state.document_container_set = ""
        st.session_state.reason_for_issue = "S2 (For information) - Used to begin co-authoring DCO submission documents"
        st.session_state.additional_notes = ""
        st.session_state.table_data = [{"Email": "LWRInformationManagement@mottmac.com"}]

