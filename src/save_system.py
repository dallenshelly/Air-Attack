"""
Save system - Handles saving and loading game data
"""

import json
import os
from datetime import datetime

class SaveSystem:
    def __init__(self):
        self.save_file = "data/data.json"
        self.default_data = {
            "User": "Player",
            "last_opendate": datetime.now().strftime("%d-%m-%Y"),
            "number_of_hours_used": "0 hr",
            "total_score": 0,
            "high_score": 0,
            "current_level": 1
        }
        
    def load_game(self):
        """Load game data from JSON file"""
        try:
            if os.path.exists(self.save_file):
                with open(self.save_file, 'r') as f:
                    data = json.load(f)
                    # Update last opened date
                    data['last_opendate'] = datetime.now().strftime("%d-%m-%Y")
                    return data
            else:
                return self.create_save_file()
        except Exception as e:
            print(f"Error loading save file: {e}")
            return self.create_save_file()
            
    def create_save_file(self):
        """Create new save file with default data"""
        try:
            os.makedirs(os.path.dirname(self.save_file), exist_ok=True)
            with open(self.save_file, 'w') as f:
                json.dump(self.default_data, f, indent=4)
            return self.default_data.copy()
        except Exception as e:
            print(f"Error creating save file: {e}")
            return self.default_data.copy()
            
    def save_game(self, data):
        """Save game data to JSON file"""
        try:
            # Calculate total hours played
            hours_str = data.get('number_of_hours_used', '0 hr')
            hours = int(hours_str.split()[0]) if hours_str.split()[0].isdigit() else 0
            # Add 1 hour for this session (you'd want to track actual playtime)
            data['number_of_hours_used'] = f"{hours + 1} hr"
            
            # Save to file
            with open(self.save_file, 'w') as f:
                json.dump(data, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving game: {e}")
            return False
            
    def update_stats(self, score, level):
        """Update game statistics"""
        data = self.load_game()
        data['total_score'] += score
        if score > data['high_score']:
            data['high_score'] = score
        data['current_level'] = level
        self.save_game(data)
        return data