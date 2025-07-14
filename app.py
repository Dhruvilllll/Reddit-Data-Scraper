import streamlit as st
import os
from scraper import fetch_user_content, save_to_file
from persona_generator import load_user_raw_text, generate_persona, save_persona
from dotenv import load_dotenv

# Load secrets
load_dotenv()

# UI Setup
st.set_page_config(page_title="Reddit Persona Generator", page_icon="🤖")
st.title("🤖 Reddit Persona Generator")
st.markdown("Scrape a Reddit user's activity and generate a Gemini-powered AI persona.")

# Input
username = st.text_input("Enter Reddit username (no 'u/' prefix):")

if username:
    st.write(f"🔗 https://www.reddit.com/user/{username}/")

    # Button 1: Scrape
    if st.button("🔍 Scrape Reddit Data"):
        with st.spinner("Scraping data..."):
            try:
                posts, comments = fetch_user_content(username, limit=100)
                if not posts and not comments:
                    st.warning("No posts/comments found. Try a different user.")
                else:
                    save_to_file(username, posts, comments)
                    st.success("✅ Data scraped successfully!")
            except Exception as e:
                st.error(f"❌ Scraping failed: {e}")

    # Button 2: Generate Persona
    if st.button("🤖 Generate Persona"):
        raw_file = f"raw_data/{username}_raw.txt"
        if not os.path.exists(raw_file):
            st.error("❌ No raw data found. Please scrape first.")
        else:
            with st.spinner("Generating persona with Gemini..."):
                try:
                    raw = load_user_raw_text(username)
                    if not raw.strip():
                        st.error("❌ Raw file is empty.")
                    else:
                        persona = generate_persona(raw, username)
                        print("Generated Persona:\n", persona)
                        if persona.strip():
                            save_path = save_persona(username, persona)
                            st.success("✅ Persona generated!")

                            st.subheader("🧠 User Persona")
                            st.text_area("Persona Output", value=persona, height=400)

                            with open(save_path, "r", encoding="utf-8") as f:
                                st.download_button("📥 Download Persona", data=f, file_name=os.path.basename(save_path))
                        else:
                            st.error("❌ Gemini returned no result.")
                except Exception as e:
                    st.error(f"❌ Persona generation failed: {e}")
