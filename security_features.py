import os

class EnterpriseShield:

    def __init__(self):
        self.notification_timer = 0

    def notify(self, title, text):
        os.system("""
                  osascript -e 'display notification "{}" with title "{}"'
                  """.format(text, title))

    def notify_reset_timer(self, name):
        if self.notification_timer <= 0 and name.lower() == "unknown":
            self.notification_timer = 60
            self.notify("Shoulder Surfing Detected", "Quick behind you!")
        else:
            self.notification_timer -= 1
