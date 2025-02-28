APP_READY: bool = False  # will be True once main app window is visible


def set_ready(flag: bool):
    global APP_READY
    APP_READY = flag
