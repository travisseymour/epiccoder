import sys
import subprocess
import darkdetect


def is_linux_dark_mode():
    try:
        # Check for GNOME dark mode
        gnome_mode = subprocess.run(
            ["gsettings", "get", "org.gnome.desktop.interface", "color-scheme"], capture_output=True, text=True
        ).stdout.strip()
        if gnome_mode in ("'prefer-dark'", "'prefer-dark'"):
            return True

        # Check for KDE dark mode
        kde_mode = (
            subprocess.run(
                ["kwriteconfig5", "--file", "kdeglobals", "--group", "KDE", "--key", "LookAndFeelPackage"],
                capture_output=True,
                text=True,
            )
            .stdout.strip()
            .lower()
        )
        if "dark" in kde_mode:
            return True

    except FileNotFoundError:
        pass  # gsettings or kwriteconfig5 not found, assume light mode

    return False


def is_dark_mode():
    if sys.platform == "win32" or sys.platform == "darwin":
        return darkdetect.isDark()
    elif sys.platform == "linux":
        return is_linux_dark_mode()
    return False


if __name__ == "__main__":
    if is_dark_mode():
        print("Dark mode is enabled")
    else:
        print("Light mode is enabled")
