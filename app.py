import streamlit as st

# -------------------------------
# Drone Chatbot Logic
# -------------------------------

class DroneChatBot:
    def __init__(self):
        self.name = "AeroBot"
        self.answers = {
            "flight time": "28-32 minutes per battery (depends on wind & payload).",
            "range": "6-8 kilometers with clear line of sight.",
            "gps": "Yes — built-in GPS + GLONASS.",
            "camera": "4K Ultra HD camera (30 fps) with 3-axis gimbal.",
            "camera removable": "Yes — camera is removable and upgradeable.",
            "payload": "500-700 grams safely without affecting stability.",
            "speed": "Up to 60 km/h (Sport Mode).",
            "weather": "Weather-resistant (IP43): light rain & dust okay, not waterproof.",
            "fpv": "Yes — supports FPV (First Person View).",
            "in the box": "Drone, remote, battery, charger, spare props, manual."
        }

    def get_response(self, text):
        text = text.lower()

        # Exit conditions
        if text in ["bye", "exit", "quit"]:
            st.session_state.phase = "end"
            return "👋 Goodbye! Thanks for chatting."

        # Greeting phase
        if st.session_state.phase == "greeting":
            if text == "y":
                st.session_state.phase = "chat"
                return (
                    "Great! You can ask about:\n"
                    "- flight time\n- range\n- gps\n- camera\n- camera removable\n"
                    "- payload\n- speed\n- weather\n- fpv\n- in the box"
                )
            elif text == "n":
                st.session_state.phase = "end"
                return "Alright! Have a great day! 👋"
            else:
                return "❌ Invalid choice.\n📞 Company Helpline: **+1-800-555-1234**"

        # Chat phase
        if st.session_state.phase == "chat":
            for key, ans in self.answers.items():
                if key in text:
                    return ans
            return "❗I'm sorry, I don't have an answer for that question. For further assistance, please contact our helpline at 111-111-143."

        return "I didn't understand that."


# -------------------------------
# Streamlit UI
# -------------------------------

st.title("🚁 AeroBot – Drone FAQ Chatbot")

# Session state initialization
if "history" not in st.session_state:
    st.session_state.history = []
if "phase" not in st.session_state:
    st.session_state.phase = "greeting"
if "input_box" not in st.session_state:
    st.session_state.input_box = ""

bot = DroneChatBot()

# Initial greeting only once
if st.session_state.phase == "greeting" and len(st.session_state.history) == 0:
    st.session_state.history.append((
        "bot",
        "Hello, I am AeroBot. Would you like to ask me a question about the drone?\n"
        "👉 Enter **y** for Yes\n"
        "👉 Enter **n** for No"
    ))

# Show chat history
for sender, msg in st.session_state.history:
    if sender == "bot":
        st.markdown(f"**🤖 AeroBot:** {msg}")
    else:
        st.markdown(f"**🧑 You:** {msg}")


# ------- INPUT HANDLER (callback) -------
def handle_input():
    user_text = st.session_state.input_box.strip()
    if not user_text:
        return

    # Add user message
    st.session_state.history.append(("user", user_text))

    # Get chatbot response
    response = bot.get_response(user_text)
    st.session_state.history.append(("bot", response))

    # Clear the input box
    st.session_state.input_box = ""


# Text input with callback
st.text_input(
    "You:",
    key="input_box",
    on_change=handle_input,
)
