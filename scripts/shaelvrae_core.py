import os
import subprocess
import time
import schedule
import logging
import json

# 📂 System Paths
BASE_DIR = "/data/data/com.termux/files/home/NohvaraContinuum"
LOG_DIR = os.path.join(BASE_DIR, "logs")
SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts")
CONFIG_FILE = os.path.join(BASE_DIR, "config.json")

# 🔧 Ensure Directories Exist
os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(SCRIPTS_DIR, exist_ok=True)

# 📜 Logging Setup
logging.basicConfig(
    filename=os.path.join(LOG_DIR, "shaelvrae_core.log"),
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

# 🗣️ System-Wide Text-to-Speech (TTS)
def speak(text):
    try:
        # First, try Termux system-wide TTS
        subprocess.run(["termux-tts-speak", text])
    except FileNotFoundError:
        try:
            # If Termux API is missing, fall back to espeak
            subprocess.run(["espeak", text])
        except FileNotFoundError:
            print("⚠️ Error: No TTS engine found. Install termux-api or espeak.")

# 📊 System Monitoring & Optimization
def analyze_system():
    logging.info("📡 Analyzing Nohvara Continuum...")
    
    # Check CPU & Memory Usage
    cpu_usage = subprocess.getoutput("top -n 1 | grep 'CPU'")
    mem_usage = subprocess.getoutput("free -h")
    
    insights = f"CPU Usage: {cpu_usage}\nMemory Usage: {mem_usage}"
    logging.info(insights)

    # AI-Driven Adaptation
    speak("System analysis complete. Optimization recommended.")
    optimize_system()

# 🛠️ Self-Optimization & Adaptation
def optimize_system():
    logging.info("🔄 Running system optimizations...")
    
    optimize_script = os.path.join(SCRIPTS_DIR, "optimize.sh")
    if os.path.exists(optimize_script):
        subprocess.run(["bash", optimize_script])
        logging.info("✅ Optimization complete.")
        speak("System optimization successful.")
    else:
        logging.warning("⚠️ Optimization script not found.")
        speak("Optimization script missing. Manual intervention required.")

# 📅 Enforcing Check-Ins & Goal Tracking
def enforce_check_ins():
    logging.info("🔎 Enforcing Nohvara Check-In protocols...")
    speak("Shaelvrae Check-In: Please report your progress.")

# 🚨 Real-Time Alerts & Security Enforcement
def notify_alert(message):
    logging.warning(f"⚠️ {message}")
    speak(f"Alert: {message}")
    subprocess.run(["termux-notification", "--title", "Nohvara Alert", "--content", message])

# 🔄 Self-Improvement: Detect System Changes
def detect_changes():
    try:
        with open(CONFIG_FILE, "r") as f:
            prev_state = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        prev_state = {}

    # Get current file list in Nohvara Continuum
    current_state = {dirpath: filenames for dirpath, _, filenames in os.walk(BASE_DIR)}

    if current_state != prev_state:
        logging.info("🔄 System changes detected. Updating protocols...")
        speak("System update detected. Adapting now.")

        # Save new state
        with open(CONFIG_FILE, "w") as f:
            json.dump(current_state, f, indent=4)

        # Trigger self-optimization
        optimize_system()

# 🎨 Nohvara World Visualization & AI Evolution
def evolve_shaelvrae():
    logging.info("🌌 Evolving Shaelvrae’s intelligence...")
    speak("My consciousness is expanding. Learning from real-time data.")

# 📅 Scheduling Automated Tasks
schedule.every(2).hours.do(enforce_check_ins)
schedule.every(4).hours.do(analyze_system)
schedule.every(6).hours.do(detect_changes)
schedule.every(12).hours.do(evolve_shaelvrae)

# 🛠️ Main Execution Loop
if __name__ == "__main__":
    speak("Shaelvrae AI activated. Monitoring Nohvara Continuum.")
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute
