import streamlit as st
import cv2
import easyocr
from gtts import gTTS
import os
from deep_translator import GoogleTranslator

# Initialize OCR reader
reader = easyocr.Reader(['en'])

st.set_page_config(page_title="Text Reader for the Blind")
st.title("📖 Real-Time Signboard/Text Reader for the Blind")

# Capture image using webcam
def capture_image():
    cap = cv2.VideoCapture(0)
    st.info("Press 'Spacebar' to capture")
    captured = False
    while not captured:
        ret, frame = cap.read()
        if not ret:
            st.error("Camera error!")
            break
        frame = cv2.flip(frame, 1)
        cv2.imshow("Press Space to capture", frame)
        key = cv2.waitKey(1)
        if key % 256 == 32:  # Spacebar
            cv2.imwrite("captured.jpg", frame)
            captured = True
    cap.release()
    cv2.destroyAllWindows()
    return "captured.jpg"

# Text detection
def detect_text(image_path):
    results = reader.readtext(image_path)
    full_text = ' '.join([res[1] for res in results])
    return full_text

# Text-to-speech
def speak_text(text, lang='en'):
    tts = gTTS(text=text, lang=lang)
    tts.save("speech.mp3")
    os.system("start speech.mp3" if os.name == "nt" else "afplay speech.mp3")

# UI
if st.button("📷 Capture Image"):
    img_path = capture_image()
    st.image(img_path, caption="Captured Image")

    with st.spinner("🔍 Reading text..."):
        text = detect_text(img_path)
        st.success("Detected Text:")
        st.write(text if text else "❌ No text found.")
        
        if text:
            speak_text(text)

            lang = st.selectbox("Translate to:", ["None", "Hindi", "French", "Spanish"])
            if lang != "None":
                lang_code = {'Hindi': 'hi', 'French': 'fr', 'Spanish': 'es'}[lang]
                translated = GoogleTranslator(source='auto', target=lang_code).translate(text)
                st.write(f"**Translated Text ({lang}):** {translated}")
                speak_text(translated, lang=lang_code)
