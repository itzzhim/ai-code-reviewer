import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(page_title="🤖 AI Code Reviewer", page_icon="🔍", layout="wide")

st.title("🤖 AI Code Reviewer")
st.markdown("Paste your code below to get instant, structured AI-powered feedback.")

# Check API key
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
if not GROQ_API_KEY:
    st.error("⚠️ GROQ_API_KEY is missing. Add it to your .env file.")
    st.stop()

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

# UI Elements
language = st.selectbox("Select Programming Language:", ["Python", "JavaScript", "Java", "C++", "C", "HTML/CSS", "SQL", "Other"])
code_input = st.text_area("Paste your code here:", height=250)

# Review Logic
if st.button("🔍 Review Code", type="primary"):
    if len(code_input.strip()) < 10:
        st.warning("⚠️ Please enter at least 10 characters of code.")
    else:
        with st.spinner("🤖 AI is analyzing your code quality, bugs, and performance..."):
            try:
                prompt = f"""You are an expert software engineer. Review the following {language} code thoroughly.
Provide your response strictly structured under these exact markdown headers:
### 🚨 Bugs & Errors
### 💡 Best Practices & Style
### ⚡ Performance Optimization
### 🛡️ Security Vulnerabilities

Be concise, precise, and actionable.

Code to review:
```{language.lower()}
{code_input}
```"""

                response = client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=[{"role": "user", "content": prompt}]
                )
                
                review_text = response.choices[0].message.content
                
                # Success state & Presentation Layout
                st.success("✅ Review Complete!")
                
                # Split layout for presentation impact
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.markdown("### 📊 Detailed Code Analysis")
                    st.markdown(review_text)
                with col2:
                    st.info("💡 **Presentation Tip**\n\nThis analysis highlights runtime bugs and optimization bottlenecks in real time using free open-source inference.")

                # Download button for the review
                st.download_button(
                    label="📥 Download Review Report",
                    data=review_text,
                    file_name="code_review_report.md",
                    mime="text/markdown"
                )

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
