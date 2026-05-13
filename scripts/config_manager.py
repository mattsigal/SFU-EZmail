import json
import os
from pathlib import Path

CONFIG_FILE = Path.home() / ".sfu_grade_applet_config.json"
CACHE_FILE = Path.home() / ".sfu_grade_applet_cache.bin"

class ConfigManager:
    @staticmethod
    def get_cache_path():
        return str(CACHE_FILE)

    @staticmethod
    def save_config(username, sender_email, subject, body):
        # Persistence disabled at user request for fresh starts
        pass

    @staticmethod
    def load_config():
        # Always return fresh defaults
        return {
            "username": "",
            "sender_email": "",
            "subject": "",
            "body": "Hello $NAME$,\n\nYou received $GRADE$ on the recent assessment.\n\nFeedback: $FEEDBACK$\n\nBest,\n[Instructor Name]"
        }
