import pathlib, os
from django.conf import settings


def logger(string, filename, dirname="common"):
    path = os.path.join(settings.BASE_DIR, "logs", dirname)
    print(path)
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)
    final_path = os.path.join(path, filename)

    with open(final_path, "w") as file:
        file.write(string + "\n")
