import streamlit as st
from gtts import gTTS
from pypdf import PdfReader
import os
import ollama


# =========================================================
# Extract text from uploaded TXT or PDF file
# =========================================================
def extract_text(file):

    if file.name.endswith(".txt"):

        return file.read().decode("utf-8")

    elif file.name.endswith(".pdf"):

        pdf_reader = PdfReader(file)

        text = ""

        for page in pdf_reader.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

        return text

    return ""


# =========================================================
# Generate speech using gTTS
# =========================================================
def generate_speech(text, language_code):

    os.makedirs("audio", exist_ok=True)

    file_path = "audio/output.mp3"

    tts = gTTS(
        text=text,
        lang=language_code
    )

    tts.save(file_path)

    return file_path


# =========================================================
# AI text enhancement using Ollama
# =========================================================
def enhance_text(text, mode):

    prompts = {

        "✨ Improve Text":
            f"""
Improve the following text while keeping its
original meaning.

Return only the improved text.

Text:
{text}
""",

        "📝 Summarize":
            f"""
Summarize the following text clearly and concisely.

Return only the summary.

Text:
{text}
""",

        "🎭 Make It Professional":
            f"""
Rewrite the following text in a professional
and natural tone.

Return only the rewritten text.

Text:
{text}
"""
    }

    response = ollama.chat(

        model="llama3.2:3b",

        messages=[
            {
                "role": "user",
                "content": prompts[mode]
            }
        ]
    )

    return response["message"]["content"]


# =========================================================
# Translate text using Ollama
# =========================================================
def translate_text(text, target_language):

    prompt = f"""
Translate the following text into {target_language}.

Keep the original meaning.

Do not explain the translation.

Return ONLY the translated text.

Text:
{text}
"""

    response = ollama.chat(

        model="llama3.2:3b",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]


# =========================================================
# Streamlit UI
# =========================================================

st.title("🔊 AI Multilingual Text-to-Speech")

st.write(
    "Convert text, TXT files, or PDF files into "
    "translated speech using Ollama and gTTS."
)


# =========================================================
# Text input
# =========================================================

text = st.text_area(

    "✍️ Enter your text:",

    placeholder=(
        "Example: Hello everyone, welcome to my project."
    ),

    height=150
)


# =========================================================
# Target language
# =========================================================

target_languages = {

    "English": "en",

    "Malay": "ms",

    "Bengali": "bn",

    "Hindi": "hi",

    "Arabic": "ar",

    "Spanish": "es",

    "French": "fr"
}


target_language_name = st.selectbox(

    "🌍 Translate & speak in:",

    list(target_languages.keys())
)


target_language_code = target_languages[
    target_language_name
]


# =========================================================
# AI processing mode
# =========================================================

ai_mode = st.selectbox(

    "🤖 Optional AI Processing:",

    [
        "None",

        "✨ Improve Text",

        "📝 Summarize",

        "🎭 Make It Professional"
    ]
)


# =========================================================
# File upload
# =========================================================

uploaded_file = st.file_uploader(

    "📄 Upload a TXT or PDF file",

    type=["txt", "pdf"]
)


# =========================================================
# Extract uploaded file
# =========================================================

uploaded_text = ""


if uploaded_file is not None:

    try:

        uploaded_text = extract_text(
            uploaded_file
        )

        if uploaded_text.strip():

            st.text_area(

                "📄 Extracted text:",

                uploaded_text,

                height=250
            )

        else:

            st.warning(
                "No readable text was found in the file."
            )

    except Exception as e:

        st.error(
            f"Could not read the file: {e}"
        )


# =========================================================
# Generate translated speech
# =========================================================

if st.button("🎙️ Translate & Generate Speech"):

    # -----------------------------------------------------
    # Determine input text
    # -----------------------------------------------------

    final_text = (
        uploaded_text
        if uploaded_text
        else text
    )


    # -----------------------------------------------------
    # Check for empty input
    # -----------------------------------------------------

    if not final_text.strip():

        st.warning(
            "Please enter text or upload a TXT/PDF file."
        )

    else:

        try:

            # -------------------------------------------------
            # Step 1: Optional AI processing
            # -------------------------------------------------

            if ai_mode != "None":

                with st.spinner(
                    "🤖 AI is processing your text..."
                ):

                    final_text = enhance_text(
                        final_text,
                        ai_mode
                    )


                st.subheader(
                    "🤖 AI-Processed Text"
                )

                st.write(
                    final_text
                )


            # -------------------------------------------------
            # Step 2: Translation
            # -------------------------------------------------

            with st.spinner(

                f"🌍 Translating to "
                f"{target_language_name}..."

            ):

                translated_text = translate_text(

                    final_text,

                    target_language_name
                )


            st.subheader(
                "🌍 Translated Text"
            )

            st.write(
                translated_text
            )


            # -------------------------------------------------
            # Step 3: Generate speech
            # -------------------------------------------------

            with st.spinner(
                "🔊 Generating speech..."
            ):

                file_path = generate_speech(

                    translated_text,

                    target_language_code
                )


            st.success(

                f"Speech generated successfully "
                f"in {target_language_name}!"
            )


            # -------------------------------------------------
            # Step 4: Audio player
            # -------------------------------------------------

            st.subheader(
                "🔊 Generated Audio"
            )

            st.audio(

                file_path,

                format="audio/mp3"
            )


            # -------------------------------------------------
            # Step 5: Download audio
            # -------------------------------------------------

            with open(
                file_path,
                "rb"
            ) as file:

                st.download_button(

                    label="⬇️ Download MP3",

                    data=file,

                    file_name=(
                        f"translated_"
                        f"{target_language_code}.mp3"
                    ),

                    mime="audio/mp3"
                )


        except Exception as e:

            st.error(
                f"Something went wrong: {e}"
            )