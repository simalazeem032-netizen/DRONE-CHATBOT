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
        Responds to the user input based on keyword matches.
        """
        text = text.lower()
        for key, ans in self.answers.items():
            if key in text:
                return ans
        return "Sorry, please ask about drone specs (flight time, range, GPS, camera, payload, etc.)."

    def show_suggestions(self):
        """Show suggested options for the user after they select 'y'."""
        print("You can ask about the following drone specs:")
        for key in self.answers:
            print(f"- {key}")

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
    run_demo()
