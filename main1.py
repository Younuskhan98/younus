import streamlit as st
import wikipedia
from PIL import Image
import requests
from io import BytesIO

# Page configuration
st.set_page_config(page_title="📚 Hey i'm V7chatbot", page_icon="📖")

# Initialize chat history before any interaction
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar: Theme toggle & Clear button
st.sidebar.title("🔧 Options")
theme = st.sidebar.selectbox("🌗 Theme", ["Light", "Dark"])
if st.sidebar.button("🧹 Clear Chat"):
    st.session_state.messages = []
    st.rerun()

# Simulated dark mode using CSS
if theme == "Dark":
    st.markdown("""
        <style>
        html, body, [class*="css"]  {
            background-color: #1e1e1e !important;
            color: #f0f0f0 !important;
        }
        .stTextInput>div>div>input {
            background-color: #333 !important;
            color: white !important;
        }
        .stButton>button {
            background-color: #333;
            color: white;
        }
        .stMarkdown {
            color: white !important;
        }
        </style>
    """, unsafe_allow_html=True)

# App title and subtitle
st.title("📚 Hey i'm V7chatbot")
st.caption("Ask me anything and I’ll fetch a short summary and image from Wikipedia!")

# Wikipedia lookup function
def get_wikipedia_summary_and_image(query):
    try:
        results = wikipedia.search(query)
        if not results:
            return "❌ Sorry, I couldn't find anything on that topic.", None

        page = wikipedia.page(results[0], auto_suggest=False, redirect=True)
        summary = wikipedia.summary(results[0], sentences=2, auto_suggest=False, redirect=True)

        image_url = None
        for img in page.images:
            if img.lower().endswith((".jpg", ".jpeg", ".png")):
                image_url = img
                break

        return summary, image_url

    except wikipedia.DisambiguationError as e:
        return f"⚠️ Your query is ambiguous. Did you mean: {', '.join(e.options[:5])}?", None
    except wikipedia.PageError:
        return "❌ Sorry, I couldn't find a page matching your query.", None
    except Exception as e:
        return "⚠️ Oops, something went wrong.", None

# User input
user_input = st.text_input("💬 Ask me anything about a topic:")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    summary, image_url = get_wikipedia_summary_and_image(user_input)
    st.session_state.messages.append({"role": "bot", "content": summary, "image": image_url})

# Display chat
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"🧑 **You:** {msg['content']}")
    else:
        st.markdown(f"🤖 **Bot:** {msg['content']}")
        if msg.get("image"):
            try:
                img_response = requests.get(msg["image"])
                img = Image.open(BytesIO(img_response.content))
                st.image(img, caption="Image from Wikipedia", use_container_width=True)
            except Exception:
                st.warning("⚠️ Couldn't load image.")
