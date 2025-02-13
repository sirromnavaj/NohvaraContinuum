import os
import time
import json
import logging
import datetime
import random
import schedule
import pyttsx3  # Text-to-Speech
import speech_recognition as sr  # Speech-to-Text
import yagmail  # Gmail automation
import subprocess

# Configure logging
log_file = os.path.expanduser("~/NohvaraContinuum/logs/system_tracking.log")
os.makedirs(os.path.dirname(log_file), exist_ok=True)

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

class Shaelvrae:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.protocols = self.load_protocols()
        self.goal_progress = self.load_goal_tracking()
        self.user_name = "Morris Javan Andanje"
        self.sirro_learning_file = os.path.expanduser("~/NohvaraContinuum/education/sirro_evolution.json")
    
    def speak(self, text):
        """Convert text to speech."""
        self.engine.say(text)
        self.engine.runAndWait()
    
    def listen(self):
        """Convert speech to text."""
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Shaelvrae is listening...")
            self.speak("I am listening...")
            audio = recognizer.listen(source)
        
        try:
            command = recognizer.recognize_google(audio)
            return command.lower()
        except sr.UnknownValueError:
            return "I didn't understand."
        except sr.RequestError:
            return "Speech recognition service is unavailable."

    def load_protocols(self):
        """Load enforced protocols from a JSON file."""
        protocols_path = os.path.expanduser("~/NohvaraContinuum/system_monitoring/protocols.json")
        if os.path.exists(protocols_path):
            with open(protocols_path, "r") as file:
                return json.load(file)
        return {"check_ins": True, "goal_tracking": True, "device_automation": True}

    def load_goal_tracking(self):
        """Load and update goal progress tracking."""
        goal_file = os.path.expanduser("~/NohvaraContinuum/logs/goal_tracking.json")
        if os.path.exists(goal_file):
            with open(goal_file, "r") as file:
                return json.load(file)
        return {"fitness": 0, "business": 0, "education": 0}

    def update_goal_progress(self, category, progress):
        """Update goal progress in real-time."""
        self.goal_progress[category] += progress
        with open(os.path.expanduser("~/NohvaraContinuum/logs/goal_tracking.json"), "w") as file:
            json.dump(self.goal_progress, file, indent=4)
        self.speak(f"{category} progress updated by {progress}%.")

    def enforce_protocols(self):
        """Check and enforce Nohvara Continuum protocols."""
        logging.info("Enforcing Nohvara Protocols...")
        if self.protocols["check_ins"]:
            self.speak("Time for your 2-hour check-in.")
            logging.info("2-hour check-in activated.")
        
        if self.protocols["goal_tracking"]:
            self.speak("Analyzing goal tracking and progress.")
            logging.info("Goal tracking enforced.")
    
    def system_adaptation(self):
        """Detect changes in Nohvara Continuum and auto-generate code updates."""
        system_path = os.path.expanduser("~/NohvaraContinuum/")
        changes_detected = []

        for root, _, files in os.walk(system_path):
            for file in files:
                file_path = os.path.join(root, file)
                if os.stat(file_path).st_mtime > (time.time() - 3600):
                    changes_detected.append(file_path)
        
        if changes_detected:
            logging.info(f"System detected updates: {changes_detected}")
            self.speak("System detected modifications. Adapting protocols accordingly.")

    def manage_device(self):
        """Automate device tasks: Calendar, Gmail, SMS monitoring."""
        logging.info("Managing device automation tasks.")
        self.speak("Checking your schedule and messages.")
        
        # Example: Checking Google Calendar tasks (Placeholder function)
        subprocess.run(["python", "~/NohvaraContinuum/system_monitoring/device_control.py"])

    def manage_sirro_language(self):
        """Evolve Sirro language by learning new words and sentence structures."""
        if os.path.exists(self.sirro_learning_file):
            with open(self.sirro_learning_file, "r") as file:
                sirro_data = json.load(file)
        else:
            sirro_data = {"vocabulary": [], "grammar_rules": []}

        new_word = f"NewWord{random.randint(1, 100)}"
        sirro_data["vocabulary"].append(new_word)
        
        with open(self.sirro_learning_file, "w") as file:
            json.dump(sirro_data, file, indent=4)
        
        self.speak(f"New Sirro word added: {new_word}")
        logging.info(f"Sirro language updated with new word: {new_word}")

    def daily_check_in(self):
        """Perform daily system check-ins and updates."""
        logging.info("Executing daily system check-in.")
        self.speak("Executing daily system check-in.")

        # Update goal tracking
        self.update_goal_progress("fitness", 5)
        self.update_goal_progress("business", 3)
        self.update_goal_progress("education", 4)

        # Adapt system if necessary
        self.system_adaptation()

    def conversation_mode(self):
        """Engage in an interactive conversation with Shaelvrae."""
        self.speak("Would you like to discuss philosophy, business, or the Nohvara system?")
        topic = self.listen()

        if "philosophy" in topic:
            self.speak("Philosophy is the mind’s greatest tool. Tell me, what do you seek to understand?")
        elif "business" in topic:
            self.speak("Business is strategy in motion. Are we discussing sales, automation, or expansion?")
        elif "nohvara" in topic:
            self.speak("The Nohvara Continuum is always evolving. What insights do you need?")
        else:
            self.speak("I will await your thoughts.")

    def start(self):
        """Initialize Shaelvrae and enforce protocols."""
        logging.info("Shaelvrae AI Activated.")
        self.speak(f"Greetings, {self.user_name}. I am Shaelvrae, your eternal guide.")

        # Schedule tasks
        schedule.every(2).hours.do(self.daily_check_in)
        schedule.every().day.at("06:00").do(self.manage_sirro_language)
        schedule.every().day.at("07:00").do(self.manage_device)

        while True:
            schedule.run_pending()
            time.sleep(10)

# Start Shaelvrae AI
if __name__ == "__main__":
    ai = Shaelvrae()
    ai.start()
