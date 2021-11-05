import re


def danger_class_definder(name):
    def work(needle):
        return name.lower().find(needle.lower()) != -1

    if work("жидкость") or work("масло") or work("смазк") or work("гермет"):
        return 3
    if work("аккум"):
        return 5

    return False


def make_brand(product):
    no_brands_ids_one = [
        "24721",
        "24429",
        "24628",
        "1296",
        "24633",
        "434",
        "527",
        "16237",
        "2479",
        "24577",
        "23704",
        "16330",
        "1681",
        "2633",
        "2305",
        "14567",
        "3226",
        "15803",
        "24813",
        "24623",
        "3547",
        "964",
        "963",
        "3615",
        "11189",
        "24352",
        "15791",
        "23318",
        "24684",
        "23850",
        "23715",
        "24194",
        "24821",
        "24698",
        "2732",
        "15583",
        "2472",
        "3443",
        "942",
        "18165",
        "2473",
        "24337",
        "21056",
        "24962",
        "24039",
        "4625",
        "24990",
        "7619",
        "23463",
        "4603",
        "25038",
        "11115",
        "16375",
        "19241",
        "25088",
        "25087",
        "22648",
        "6028",
        "6810",
        "4588",
        "21028",
        "4858",
        "15941",
        "2480",
        "18777",
        "25260",
        "25259",
        "5533",
        "17750",
        "2645",
        "15372",
        "23664",
        "15995",
        "2397",
        "15996",
        "16586",
        "832",
        "986",
        "15415",
        "23111",
        "25178",
        "8785",
        "25197",
        "8692",
        "15373",
        "8941",
        "21135",
        "15417",
        "25174",
        "15193",
        "25112",
        "25280",
        "3390",
        "1840",
        "25285",
        "22836",
        "615",
        "148",
        "15413",
        "1791",
    ]
    no_brands_ids = []
    no_brands_ids.append(no_brands_ids_one)

    brand = "original"

    try:

        brand = product.brand.brand.capitalize()
        brand = re.sub(r"[\-\/]", " ", brand)
        if not brand or brand == "оригинал":
            brand = "original"
        if brand.lower() == "mobis".lower():
            brand = "original"
    except Exception as e:
        # print("No brand found")
        pass

    if str(product.one_c_id) in no_brands_ids:
        return "Нет бренда"
    return brand
