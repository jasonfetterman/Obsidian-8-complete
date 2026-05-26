# OBSIDIAN-8 SYSTEM STATE (DERIVED MODEL)

class SystemState:
    def __init__(self, missions_ref=None):
        self.missions_ref = missions_ref
        self.state = {
            "status": "online",
            "mode": "idle",
            "alerts": []
        }

    def set_mode(self, mode):
        self.state["mode"] = mode

    def add_alert(self, alert):
        self.state["alerts"].append(alert)

    def clear_alerts(self):
        self.state["alerts"] = []

    def get_state(self):
        active = 0
        if self.missions_ref:
            active = len(self.missions_ref.list_missions())

        return {
            **self.state,
            "active_missions": active
        }