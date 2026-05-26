# OBSIDIAN-8 COMMAND CORE ENTRYPOINT (FULLY STANDARDIZED API)

from command.core import CommandRouter, MissionManager, SystemState


def bootstrap():
    router = CommandRouter()
    missions = MissionManager()
    state = SystemState(missions)

    # -------------------------
    # COMMAND HANDLERS
    # -------------------------

    def create_mission(payload):
        try:
            mission_id = missions.create_mission(payload)

            return {
                "status": "success",
                "data": {
                    "mission_id": mission_id
                }
            }

        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }

    def get_state(_):
        try:
            return {
                "status": "success",
                "data": state.get_state()
            }

        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }

    # -------------------------
    # ROUTE REGISTRATION
    # -------------------------

    router.register_route("CREATE_MISSION", create_mission)
    router.register_route("STATE", get_state)

    return router, missions, state


def run_console(router):
    print("COMMAND CORE ONLINE — FULLY STANDARDIZED MODE")
    print("Commands:")
    print("  CREATE_MISSION:{\"name\":\"TEST\"}")
    print("  STATE")
    print("  EXIT")

    while True:
        raw = input("> ").strip()

        if raw.upper() == "EXIT":
            break

        try:
            if ":" in raw:
                cmd_type, payload = raw.split(":", 1)
                payload = eval(payload)
            else:
                cmd_type = raw
                payload = {}

            result = router.dispatch({
                "type": cmd_type.strip(),
                "payload": payload
            })

            print(result)

        except Exception as e:
            print({
                "status": "error",
                "message": str(e)
            })


if __name__ == "__main__":
    router, missions, state = bootstrap()
    run_console(router)