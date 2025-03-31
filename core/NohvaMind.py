import os
import json
import time
import psutil
import subprocess
import requests
import logging
import random
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPEN_WEBUI_URL = os.getenv("OPEN_WEBUI_URL")

# Ensure required variables exist
if not BOT_TOKEN or not OPEN_WEBUI_URL:
    raise ValueError("Error: Required environment variables not set.")

# Logging Configuration
logging.basicConfig(
    filename="logs/nohva_mind.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# === CORE CLASS ===
class NohvaMind:
    def __init__(self):
        """Initialize NohvaMind Core"""
        self.start_time = datetime.now()
        self.last_optimization = None
        self.learned_commands = []
        logging.info("🔹 NohvaMind Core Initialized.")

    # === SYSTEM MONITORING ===
    def system_monitor(self):
        """Monitor system stats (Termux-compatible)."""
        usage = {
            "cpu": self.get_cpu_info(),
            "memory": self.get_memory_info(),
            "disk": self.get_disk_usage(),
            "uptime": str(datetime.now() - self.start_time)
        }
        return usage

    def get_cpu_info(self):
        """Fetch CPU usage safely."""
        try:
            return psutil.cpu_percent(interval=1)
        except Exception:
            return "CPU info unavailable"

    def get_memory_info(self):
        """Fetch memory usage safely."""
        try:
            return psutil.virtual_memory().percent
        except Exception:
            return "Memory info unavailable"

    def get_disk_usage(self):
        """Fetch disk usage safely."""
        try:
            return psutil.disk_usage('/').percent
        except Exception:
            return "Disk info unavailable"

    # === SYSTEM OPTIMIZATION ===
    def optimize_system(self):
        """Optimize system performance by freeing memory and managing tasks."""
        logging.info("⚙️ System Optimization Started.")

        # Attempt to clear cache (Linux/Android Termux specific)
        try:
            subprocess.run(["sync"], check=True)
            subprocess.run(["echo", "3", ">", "/proc/sys/vm/drop_caches"], check=True)
            logging.info("🧹 Cache cleared successfully.")
        except Exception:
            logging.warning("❌ Cache clearing failed. Root access may be required.")

        # Log completion
        logging.info("✅ System Optimization Completed.")

    # === SELF-LEARNING ===
    def learn_command(self, command):
        """Store new commands dynamically."""
        if command not in self.learned_commands:
            self.learned_commands.append(command)
            logging.info(f"🧠 Learned new command: {command}")

    def execute_learned_commands(self):
        """Execute learned commands."""
        for command in self.learned_commands:
            try:
                subprocess.run(command, shell=True, check=True)
                logging.info(f"✅ Executed learned command: {command}")
            except Exception:
                logging.warning(f"⚠️ Failed to execute: {command}")

    # === HACKER SECURITY TESTER ===
    class NohvaHacker:
        def __init__(self):
            """Simulated hacker persona to test system defenses."""
            self.attack_methods = ["brute force", "SQL injection", "DDoS simulation"]

        def attempt_attack(self):
            """Perform a simulated attack and improve defenses."""
            attack = random.choice(self.attack_methods)
            logging.warning(f"⚠️ Simulated attack detected: {attack}")
            return attack

    # === INTELLIGENT SELF-OPTIMIZATION ===
    def search_for_improvements(self):
        """Fetch optimization techniques from the web (simulated)."""
        try:
            response = requests.get("https://api.example.com/optimizations")  # Placeholder URL
            optimizations = response.json()
            logging.info(f"🔍 Found new optimizations: {optimizations}")
            return optimizations
        except Exception:
            logging.warning("❌ Failed to retrieve optimizations.")
            return []

# === RUN SYSTEM MONITOR ===
if __name__ == "__main__":
    nohva = NohvaMind()
    print(nohva.system_monitor())
    nohva.optimize_system()

    # Simulate self-learning
    nohva.learn_command("echo 'Hello, NohvaMind!'")
    nohva.execute_learned_commands()

    # Simulate hacker testing
    hacker = nohva.NohvaHacker()
    hacker.attempt_attack()

    # Simulate self-improvement
    nohva.search_for_improvements()
