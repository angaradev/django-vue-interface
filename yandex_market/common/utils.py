def danger_class_definder(name):
    def work(needle):
        return name.lower().find(needle.lower()) != -1

    if work("жидкость") or work("масло") or work("смазк") or work("гермет"):
        return 3
    if work("аккум"):
        return 5

    return False
