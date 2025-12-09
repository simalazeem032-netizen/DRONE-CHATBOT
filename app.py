import streamlit as st

# ================================
# YOUR ORIGINAL CODE (UNCHANGED)
# ================================

# Simple OOP Drone FAQ Chatbot (Very Basic)
class Greeting:
    """
    Base class that handles the greeting and asks if the user wants to ask a question.
    """
    def __init__(self, name):
        self.name = name

    def greeting(self):
        """Print a simple greeting and ask if the user wants to ask a question."""
        print(f"Hello, I am {self.name}. Would you like to ask me a question about the drone?")
        print("y. Yes")
        print("n. No")
        
    def ask_question(self):
        """Ask the user if they want to ask a question."""
        user_input = input("Your choice (y or n): ").strip().lower()
        if user_input == 'y':
            return True
        elif user_input == 'n':
            print("Bot: Okay, have a great day!")
            return False
        else:
            print("Bot: Invalid choice. Please choose 'y' or 'n'.")
            return self.ask_question()

class ChatBot(Greeting):
    """
    Base chatbot class.
    Holds the bot name and defines a basic greeting method.
    """
    def __init__(self, name):
        super().__init__(name)

    def greeting(self):
        """Print a simple greeting."""
        super().greeting()  # Call the greeting from the Greeting class

class DroneChatBot(ChatBot):
    """
    DroneChatBot inherits from ChatBot.
    It stores simple keyword-response pairs and answers user questions.
    """
    def __init__(self, name):
        super().__init__(name)
        # Simple dictionary of keywords to answers
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
        """
        Responds to the user input based on keyword matches, and provides recommendations.
        """
        text = text.lower()
        
        # --- MODIFICATION 2: Expanded Conditional Recommendations ---
        recommendation = ""
        if "speed" in text:
            recommendation = " If high speed is your priority, consider the **Drone 4590**."
        elif "flight time" in text or "battery" in text:
            recommendation = " For extended battery life, the **Drone 7896** is an excellent choice."
        elif "weather" in text:
            recommendation = " For better weather resistance and durability, check out the **Drone 210B**."
        elif "fpv" in text:
            recommendation = " For an immersive FPV experience, we recommend the agile **Drone FPV-X**."
        elif "gps" in text or "positioning" in text:
            recommendation = " For the most reliable and accurate GPS, look at the **Drone GeoPro**."
        elif "range" in text or "distance" in text:
            recommendation = " For maximum operational range, the **Drone LR-900** is the best option."
        # -----------------------------------------------------------------

        for key, ans in self.answers.items():
            if key in text:
                return ans + recommendation # Append the recommendation to the answer
        
        # If no specific spec answer is found, return the generic message (without recommendation)
        return "Sorry, please ask about drone specs (flight time, range, GPS, camera, payload, etc.)."

    def show_suggestions(self):
        """Show suggested options for the user after they select 'y'."""
        print("---")
        print("You can ask about the following drone specs:")
        for key in self.answers:
            print(f"- {key}")
        # --- MODIFICATION 1: Quit Instructions ---
        print("\nType 'exit', 'quit', or 'bye' to end the chat.")
        print("---")
        # -----------------------------------------

def run_demo():
    bot = DroneChatBot("AeroBot")
    bot.greeting()  # Initial greeting
    if bot.ask_question():  # Check if the user wants to ask a question
        bot.show_suggestions()  # Show suggestions immediately after "y"
        while True:
            user = input("You: ").strip()
            if user.lower() in ("exit", "quit", "bye"):
                print("Bot: Goodbye!")
                break
            response = bot.get_response(user)
            print("Bot:", response)
            # If the response is a suggestion message, show options for the user
            if "Sorry" in response:
                bot.show_suggestions()
    else:
        print("Bot: Goodbye!")

if __name__ == "__main__":
    # This block is ignored by Streamlit, but kept for console use.
    pass
    # run_demo()


# ================================
# STREAMLIT UI (NEW WRAPPER CODE)
# ================================

st.title("🚁 AeroBot – Drone FAQ Chatbot")

# --- Initialize session state ---
if "bot" not in st.session_state:
    st.session_state.bot = DroneChatBot("AeroBot")

if "history" not in st.session_state:
    st.session_state.history = []

if "phase" not in st.session_state:
    # "greeting" -> waiting for y/n
    # "chat"     -> normal Q&A
    # "end"      -> finished
    st.session_state.phase = "greeting"

if "input_box" not in st.session_state:
    st.session_state.input_box = ""

bot = st.session_state.bot

# --- Initial greeting (mimics your Greeting.greeting text) ---
if st.session_state.phase == "greeting" and len(st.session_state.history) == 0:
    greeting_msg = (
        f"Hello, I am {bot.name}. Would you like to ask me a question about the drone?\n"
        "y. Yes\n"
        "n. No"
    )
    st.session_state.history.append(("bot", greeting_msg))


# Helper to mimic show_suggestions() output, but as a message instead of print()
def suggestions_message():
    lines = []
    lines.append("---")
    lines.append("You can ask about the following drone specs:")
    for key in bot.answers:
        lines.append(f"- {key}")
    lines.append("\nType 'exit', 'quit', or 'bye' to end the chat.")
    lines.append("---")
    return "\n".join(lines)


# --- Input handler (callback) ---
def handle_input():
    user_text = st.session_state.input_box.strip()
    if not user_text:
        return

    # Add user message
    st.session_state.history.append(("user", user_text))

    # Phase: greeting -> expect 'y' or 'n'
    if st.session_state.phase == "greeting":
        choice = user_text.lower()
        if choice == "y":
            st.session_state.phase = "chat"
            # Show suggestions (equivalent to bot.show_suggestions, but as text)
            st.session_state.history.append(("bot", suggestions_message()))
        elif choice == "n":
            st.session_state.phase = "end"
            st.session_state.history.append(("bot", "Okay, have a great day!"))
        else:
            st.session_state.history.append(("bot", "Invalid choice. Please choose 'y' or 'n'."))

    # Phase: chat -> normal Q&A using your get_response()
    elif st.session_state.phase == "chat":
        if user_text.lower() in ("exit", "quit", "bye"):
            st.session_state.phase = "end"
            st.session_state.history.append(("bot", "Goodbye!"))
        else:
            response = bot.get_response(user_text)
            st.session_state.history.append(("bot", response))
            # If generic "Sorry" appears, show suggestions like in your console version
            if "Sorry" in response:
                st.session_state.history.append(("bot", suggestions_message()))

    # Phase: end -> just inform user
    else:
        st.session_state.history.append(
            ("bot", "Chat has ended. Refresh the page to start again.")
        )

    # Clear the input box
    st.session_state.input_box = ""


# --- Show chat history ---
for sender, msg in st.session_state.history:
    if sender == "bot":
        st.markdown(f"**🤖 Bot:** {msg}")
    else:
        st.markdown(f"**🧑 You:** {msg}")

# --- Text input with callback ---
st.text_input(
    "You:",
    key="input_box",
    on_change=handle_input,
)
