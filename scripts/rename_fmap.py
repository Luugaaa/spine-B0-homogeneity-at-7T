import os
import re

ROOT_DIR = "data"

for dirpath, _, filenames in os.walk(ROOT_DIR):
    for filename in filenames:
        new_name = re.sub(r"-2(\.[^.]+)$", r"\1", filename)
        if new_name != filename:
            os.rename(
                os.path.join(dirpath, filename),
                os.path.join(dirpath, new_name)
            )
            print(f"{filename} → {new_name}")
