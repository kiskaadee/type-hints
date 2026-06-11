"""
Glow integration helper.

Responsible for:
    - detecting if the 'glow' markdown renderer is installed
    - providing OS-specific installation commands
"""

import shutil
import sys


def is_glow_available() -> bool:
    """Returns True if the 'glow' command-line binary is available on the system PATH."""
    return shutil.which("glow") is not None


def get_glow_install_advice() -> str:
    """Returns OS-specific installation instructions for Glow."""
    platform = sys.platform
    if platform.startswith("linux"):
        return (
            "To install Glow on Linux:\n"
            "  - Ubuntu/Debian: sudo apt install glow (or visit https://github.com/charmbracelet/glow)\n"
            "  - Arch Linux:    sudo pacman -S glow\n"
            "  - Fedora/RHEL:   sudo dnf install glow\n"
            "  - Homebrew:      brew install glow"
        )
    elif platform == "darwin":
        return (
            "To install Glow on macOS:\n"
            "  - Homebrew: brew install glow\n"
            "  - MacPorts: sudo port install glow"
        )
    elif platform == "win32":
        return (
            "To install Glow on Windows:\n"
            "  - Winget: winget install Charmbracelet.Glow\n"
            "  - Scoop:  scoop install glow\n"
            "  - Chocolatey: choco install glow"
        )
    else:
        return "Please visit https://github.com/charmbracelet/glow for installation instructions."
