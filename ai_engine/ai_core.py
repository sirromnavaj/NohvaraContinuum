import os
import logging
import json
import subprocess

# Use the existing logs directory in NohvaraContinuum
log_dir = os.path.abspath(os.path.join(os.getcwd(), "../logs"))  
log_file = os.path.join(log_dir, "ai_core.log")

# Ensure the logs directory exists
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Configure logging
logging.basicConfig(filename=log_file, level=logging.INFO, format="%(asctime)s - %(message)s")

class AICore:
    def __init__(self):
        self.load_settings()

    def load_settings(self):
        """Load system settings from a JSON config file."""
        config_path = os.path.abspath(os.path.join(os.getcwd(), "../system_monitoring/settings.json"))
        if os.path.exists(config_path):
            with open(config_path, "r") as file:
                self.settings = json.load(file)
        else:
            self.settings = {"optimization_level": "medium"}
            self.save_settings()

    def save_settings(self):
        """Save settings to file."""
        config_path = os.path.abspath(os.path.join(os.getcwd(), "../system_monitoring/settings.json"))
        with open(config_path, "w") as file:
            json.dump(self.settings, file, indent=4)

    def analyze_and_improve(self):
        """Analyze system performance and optimize processes."""
        logging.info("🔍 AI is analyzing system data...")
        self.optimize_system()
        self.update_ai_models()

    def optimize_system(self):
        """Optimize system processes based on detected inefficiencies."""
        logging.info("⚙️ Optimizing system processes...")
        subprocess.run(["bash", "../scripts/optimize.sh"], check=True)
        logging.info("✅ System optimization complete.")

    def execute_protocols(self):
        """Execute required system protocols."""
        logging.info("🚀 Executing system protocols...")
        subprocess.run(["bash", "../scripts/execute_protocols.sh"], check=True)
        logging.info("✅ Protocol execution complete.")

    def update_ai_models(self):
        """Train and improve AI models in real-time."""
        logging.info("🤖 Updating AI models with real-time data...")
        subprocess.run(["python", "../ai_engine/train_models.py"], check=True)
        logging.info("✅ AI models updated.")

# If run directly, initialize AI Core
if __name__ == "__main__":
    ai = AICore()
    ai.analyze_and_improve()
    ai.execute_protocols()
