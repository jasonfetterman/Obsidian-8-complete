# OBSIDIAN-8 COMMAND LAYER
# Command Router — receives and routes all system-level instructions

class CommandRouter:
    def __init__(self):
        self.routes = {}
        self.active = True

    def register_route(self, command_type, handler):
        """Register a command handler"""
        self.routes[command_type] = handler

    def dispatch(self, command):
        """
        Dispatch incoming command to the correct handler.
        Command format: {
            "type": str,
            "payload": dict
        }
        """
        if not self.active:
            return {"status": "inactive"}

        cmd_type = command.get("type")

        if cmd_type not in self.routes:
            return {
                "status": "error",
                "message": f"Unknown command type: {cmd_type}"
            }

        return self.routes[cmd_type](command.get("payload", {}))

    def shutdown(self):
        self.active = False

    def restart(self):
        self.active = True