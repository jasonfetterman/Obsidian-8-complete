# OBSIDIAN-8 MISSION MANAGER
# Handles mission lifecycle: creation, tracking, completion

class MissionManager:
    def __init__(self):
        self.missions = {}
        self.counter = 0

    def create_mission(self, mission_data):
        mission_id = f"M-{self.counter}"
        self.counter += 1

        self.missions[mission_id] = {
            "data": mission_data,
            "status": "active"
        }

        return mission_id

    def update_status(self, mission_id, status):
        if mission_id in self.missions:
            self.missions[mission_id]["status"] = status
            return True
        return False

    def get_mission(self, mission_id):
        return self.missions.get(mission_id, None)

    def list_missions(self):
        return self.missions