import streamlit as st
import cv2
import mediapipe as mp
import pyautogui
import numpy as np

# إعدادات الصفحة
st.set_page_config(page_title="Shortcut AI App", layout="wide")

st.title("🚀 تطبيق التحكم الذكي (Streamlit Edition)")
st.sidebar.title("القائمة الرئيسية")
choice = st.sidebar.selectbox("اختر نمط التحكم:", ["الرئيسية", "التحكم باليد", "التحكم بالعين", "كاشف الجسم"])

# إعدادات ميديا بايب
mp_hands = mp.solutions.hands
mp_face_mesh = mp.solutions.face_mesh
screen_w, screen_h = pyautogui.size()


def run_hand_control():
    st.subheader("التحكم بالماوس عن طريق اليد")
    run = st.checkbox("تشغيل الكاميرا", value=True)
    FRAME_WINDOW = st.image([])  # مكان عرض الفيديو

    cam = cv2.VideoCapture(0)
    hands = mp_hands.Hands()

    while run:
        ret, frame = cam.read()
        if not ret: break

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                index_finger = hand_landmarks.landmark[8]
                thumb_finger = hand_landmarks.landmark[4]

                # تحريك الماوس الحقيقي
                pyautogui.moveTo(int(index_finger.x * screen_w), int(index_finger.y * screen_h))

                # النقر
                if abs(index_finger.y - thumb_finger.y) < 0.05:
                    pyautogui.click()
                    st.toast("تم النقر! ✅")

        # عرض الفيديو داخل Streamlit
        FRAME_WINDOW.image(rgb)
    else:
        cam.release()


def run_eye_control():
    st.subheader("التحكم بالماوس عن طريق العين (الأنف والغمزة)")
    run = st.checkbox("تشغيل الكاميرا", value=True)
    FRAME_WINDOW = st.image([])

    cam = cv2.VideoCapture(0)
    face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

    while run:
        ret, frame = cam.read()
        if not ret: break

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb)

        if results.multi_face_landmarks:
            face = results.multi_face_landmarks[0]
            nose = face.landmark[1]
            pyautogui.moveTo(int(nose.x * screen_w), int(nose.y * screen_h))

            # الغمزة
            top = face.landmark[159];
            bottom = face.landmark[145]
            if abs(top.y - bottom.y) < 0.01:
                pyautogui.click()
                pyautogui.sleep(0.2)

        FRAME_WINDOW.image(rgb)
    else:
        cam.release()


# توجيه المستخدم بناءً على الخيار
if choice == "الرئيسية":
    st.write("أهلاً بك في تطبيقك الخاص. اختر نمط التشغيل من القائمة الجانبية.")
    st.info("تأكد من إعطاء صلاحيات Accessibility لبرنامج الـ Terminal أو الـ IDE.")

elif choice == "التحكم باليد":
    run_hand_control()

elif choice == "التحكم بالعين":
    run_eye_control()

elif choice == "كاشف الجسم":
    st.warning("هذه الخاصية قيد التطوير في نسخة Streamlit")
