import subprocess
import platform


def notify_user():
    """
    Bubble notification in windows
    """
    p = subprocess.Popen(["powershell", "./powershell_scripts/notification.ps1"], stdout=subprocess.PIPE)


def hide_windows():
    """
    Just toggles the show desktop action. It can be used to both show
    or hide windows when used in succession.
    """
    p = subprocess.Popen(["powershell", "./powershell_scripts/hideWindows.ps1"], stdout=subprocess.PIPE)


def lock_screen():
    """
    Locks the screen
    """
    p = subprocess.Popen(["powershell", "./powershell_scripts/lockscreen.ps1"], stdout=subprocess.PIPE)


if __name__ == '__main__':
    # Simple command that returns the current OS details
    print(platform.platform())
