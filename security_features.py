import os, pwd
class EnterpriseShield:

    def __init__(self):
        self.notification_timer = 0


    def notify(self, title, text):
        ''' executes apple script to generate system timer'''
        os.system("""
                  osascript -e 'display notification "{}" with title "{}"'
                  """.format(text, title))


    def notify_reset_timer(self, name):
        ''' Resets timer to show system notification '''
        if self.notification_timer <= 0 and name.lower() == "unknown":
            self.notification_timer = 60
            self.notify("Shoulder Surfing Detected", "Quick behind you!")
        else:
            self.notification_timer -= 1


    def hide_windows(self):
        ''' executes apple script to hide all active windows. '''
        os.system("""
        osascript -e 'tell application "System Events" to set visible of every application process to false'
                """)


    def show_windows(self):
        ''' executes apple script to show all active windows. '''
        os.system("""
        osascript -e 'tell application "System Events" to set visible of every application process to true'
                """)


    def get_username(self):
        ''' Returns the currently signed in username as <string> '''
        return pwd.getpwuid( os.getuid() )[ 0 ]
    

    def lock_screen(self):
        ''' executes apple script to lock the screen and require user to login again '''
        os.system("""
        osascript -e 'tell application "Finder" to sleep'
                """)