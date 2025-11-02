import streamlit as st
import pyzipper
import io

st.set_page_config(page_title="File Encryptor", page_icon="🔒", layout="centered")

st.title("🔐 File Encryptor (Password Protected Zip)")
st.write("Upload any file, set a password, and download a securely encrypted zip file that you can open anywhere.")

uploaded_file = st.file_uploader("📂 Upload any file", type=None)
password = st.text_input("🔑 Enter Password", type="password")

if st.button("Encrypt File"):
    if not uploaded_file:
        st.error("⚠️ Please upload a file first.")
    elif not password:
        st.error("⚠️ Please enter a password.")
    else:
        # Read the uploaded file
        file_data = uploaded_file.read()

        # Create encrypted ZIP in memory
        zip_buffer = io.BytesIO()
        with pyzipper.AESZipFile(zip_buffer,
                                 'w',
                                 compression=pyzipper.ZIP_DEFLATED,
                                 encryption=pyzipper.WZ_AES) as zf:
            zf.setpassword(password.encode())
            zf.setencryption(pyzipper.WZ_AES, nbits=256)  # AES-256 encryption
            zf.writestr(uploaded_file.name, file_data)

        zip_buffer.seek(0)

        # Encrypted file name
        encrypted_name = uploaded_file.name + "_encrypted.zip"

        # Provide download
        st.success("✅ File successfully encrypted!")
        st.download_button(
            label="⬇️ Download Encrypted File",
            data=zip_buffer,
            file_name=encrypted_name,
            mime="application/zip"
        )

        st.info("You can open this encrypted zip file in any file manager or unzip tool by entering your password.")

st.markdown("---")
st.caption("🔰 Encryption: AES-256 (ZIP format, compatible with WinZip, 7-Zip, ZArchiver, etc.)")
