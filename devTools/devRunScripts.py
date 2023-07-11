import os

from packages.utils import getNowUnixTimestamp


def cleanLogs():
    basedir = os.path.dirname(__file__)
    basedir = os.path.dirname(basedir)
    now = getNowUnixTimestamp()
    for f in os.listdir(os.path.join(basedir, "log")):
        if f.endswith(".log") and f.startswith("debug_"):
            file_timestamp = int(float(f.replace("debug_", "").replace(".log", "")))

            if now - file_timestamp > 60 * 60 * 24:
                os.remove(os.path.join(basedir, "log", f))
                print(f"Delete {f}")


print("Start pre init script.")
cleanLogs()
