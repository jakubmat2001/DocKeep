import sys
import os
import shutil
from pathlib import Path

def resource_path(relative_path):
    """Locate bundled, read-only application resources."""

    if getattr(sys, "frozen", False):
        base_path = Path(sys._MEIPASS)
    else:
        base_path = Path(__file__).resolve().parent.parent

    return base_path / relative_path


def data_path(filename):
    """Locate writable application data."""

    if not getattr(sys, "frozen", False):
        return resource_path(filename)

    if sys.platform == "darwin":
        base_path = (
            Path.home()
            / "Library"
            / "Application Support"
            / "DocKeep"
        )
    elif os.name == "nt":
        base_path = (
            Path(os.environ.get("APPDATA", Path.home()))
            / "DocKeep"
        )
    else:
        base_path = (
            Path.home()
            / ".local"
            / "share"
            / "DocKeep"
        )

    base_path.mkdir(parents=True, exist_ok=True)

    destination = base_path / filename

    # Initialise user data from the bundled defaults.
    if not destination.exists():
        source = resource_path(filename)

        if source.is_file():
            shutil.copy2(source, destination)

    return destination