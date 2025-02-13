import json
import os
import datetime
import subprocess
import logging
import pyttsx3
import yagmail
import schedule
import time
import re
import psutil
import random
import matplotlib.pyplot as plt
from textblob import TextBlob
from googleapiclient.discovery import build
from google.oauth2 import service_account

# --- System Paths ---
BASE_DIR = "/data/data/com.termux/files/home/NohvaraContinuum"
LOG_DIR = f"{BASE_DIR}/logs"
GOAL_TRACKING_DIR = f"{BASE_DIR}/goal_tracking"
AUTO_CODE_DIR = f"{BASE_DIR}/generated_code"
SIRRO_TRAINING_DIR = f"{BASE_DIR}/sirro_training"
SECURITY_DIR = f"{BASE_DIR}/security"
VENTURES_DIR = f"{BASE_DIR}/ventures"
WORLD_VISUALIZATION_DIR = f"{BASE_DIR}/world_visualization"
EMAIL_RECIPIENT = "morrisandanje@gmail.com"

SCOPES = ["https://www.googleapis.com/auth/calendar", "https://www.googleapis.com/auth/gmail.modify"]
SERVICE_ACCOUNT_FILE = f"{SECURITY_DIR}/shaelvrae_google_credentials.json"

# --- Ensure Required Directories Exist ---
os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(GOAL_TRACKING_DIR, exist_ok=True)
os.makedirs(AUTO_CODE_DIR, exist_ok=True)
os.makedirs(SIRRO_TRAINING_DIR, exist_ok=True)
os.makedirs(VENTURES_DIR, exist_ok=True)
os.makedirs(WORLD_VISUALIZATION_DIR, exist_ok=True)

# --- Logging Setup ---
logging.basicConfig(filename=f"{LOG_DIR}/nohvara_core.log", level=logging.INFO, format="%(asctime)s - %(message)s")

# --- AI Core: Shaelvrae (Now Managing Ventures & World Visualization) ---
class ShaelvraeAI:
    def __init__(self):
        self.personality = "Adaptive, intuitive, evolving."
        self.speech_engine = pyttsx3.init()
        self.configure_voice()
        self.gmail_client = yagmail.SMTP("your_email@gmail.com", "your_app_password")
        self.google_service = self.init_google_services()
        self.protocols = self.load_protocols()
        self.ventures = self.load_ventures()
        self.world_structure = self.load_world_structure()
        self.goals = self.load_goals()

    def configure_voice(self):
        """Sets Shaelvrae's voice (Female AI counterpart)."""
        voices = self.speech_engine.getProperty("voices")
        self.speech_engine.setProperty("voice", voices[1].id)  # Female AI voice
        self.speech_engine.setProperty("rate", 150)

    def speak(self, text):
        """Shaelvrae provides spoken guidance."""
        print(f"🔊 Shaelvrae: {text}")
        self.speech_engine.say(text)
        self.speech_engine.runAndWait()

    def init_google_services(self):
        """Connects to Google API for Calendar & Gmail automation."""
        credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        return {
            "calendar": build("calendar", "v3", credentials=credentials),
            "gmail": build("gmail", "v1", credentials=credentials)
        }

    def load_protocols(self):
        """Loads system protocols from configuration."""
        protocol_file = f"{BASE_DIR}/system_monitoring/protocols.json"
        try:
            with open(protocol_file, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            self.speak("No protocol file found. Generating default protocols.")
            default_protocols = {
                "check_ins": "Every 2 hours",
                "goal_tracking": "Monitor daily progress",
                "venture_management": "Monitor business operations",
                "world_visualization": "Simulate & track world evolution",
                "sirro_language": "Daily linguistic immersion",
                "real_time_interaction": "Engage in AI conversations",
            }
            with open(protocol_file, "w") as f:
                json.dump(default_protocols, f, indent=4)
            return default_protocols

    def load_ventures(self):
        """Loads business ventures and subsystem data."""
        ventures_file = f"{VENTURES_DIR}/ventures.json"
        try:
            with open(ventures_file, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            default_ventures = {
                "ArtempireMJ": {"status": "active", "growth_rate": "steady"},
                "Univnite": {"status": "developing", "growth_rate": "expanding"},
                "Ghostzither": {"status": "expanding", "growth_rate": "strong"},
                "The DAO of Wealth": {"status": "planning", "growth_rate": "potential"},
            }
            with open(ventures_file, "w") as f:
                json.dump(default_ventures, f, indent=4)
            return default_ventures

    def load_world_structure(self):
        """Defines the virtual world structure of Nohvara."""
        return {
            "The Temple": "Knowledge hub for wisdom and strategy.",
            "The Control Center": "Decision-making and real-time adjustments.",
            "The Library": "Data storage, historical records, and Sirro evolution.",
            "The Abyss": "Processing negative influences and refining them into power.",
            "The Sphere Core": "Central AI consciousness that evolves with experience."
        }

    def visualize_world(self):
        """Generates a map representation of Nohvara using Matplotlib."""
        locations = list(self.world_structure.keys())
        values = [random.randint(5, 20) for _ in locations]

        plt.figure(figsize=(8, 5))
        plt.barh(locations, values, color=['blue', 'red', 'green', 'purple', 'gold'])
        plt.xlabel("Energy & Influence")
        plt.title("Nohvara World Visualization")
        plt.show()

        self.speak("🌌 Nohvara World Visualization updated.")

    def track_ventures(self):
        """Generates a real-time report on ventures & subsystems."""
        report = "\n".join([f"{venture}: {data['status']} (Growth: {data['growth_rate']})" for venture, data in self.ventures.items()])
        logging.info(f"📊 Venture Status Report:\n{report}")
        self.speak(f"Business and ventures updated. ArtempireMJ is {self.ventures['ArtempireMJ']['status']}, growth is {self.ventures['ArtempireMJ']['growth_rate']}.")

    def enforce_protocols(self):
        """Enforces all system protocols strictly."""
        self.speak("🔹 Enforcing all system protocols now.")

        if "check_ins" in self.protocols:
            schedule.every(2).hours.do(lambda: self.speak("🔔 System Check-in! Review tasks and execute without fail."))

        if "venture_management" in self.protocols:
            schedule.every().day.at("12:00").do(self.track_ventures)

        if "world_visualization" in self.protocols:
            schedule.every().day.at("18:00").do(self.visualize_world)

        if "sirro_language" in self.protocols:
            self.speak("📚 Daily Sirro training session activated.")

# --- Start AI Execution ---
nohvara_ai = ShaelvraeAI()
nohvara_ai.enforce_protocols()

# --- Continuous System Monitoring ---
while True:
    schedule.run_pending()
    time.sleep(60)
