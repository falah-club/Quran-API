import os
import json


def makeDir(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)


def makeJson(path, content):
    with open(path, "w", encoding="utf8") as file:
        json.dump(content, file, ensure_ascii=0, indent=4)


def readJsonFile(path: str):
    with open(f"Data/{path}", "r", encoding="utf8") as file:
        return json.load(file)


if os.path.exists("public"):
    os.chdir("public")

reciters = {
    "1": "Mishary Rashid Al-Afasy",
    "2": "Abu Bakr Al-Shatri",
    "3": "Nasser Al Qatami",
}
originalUrl = {
    "1": "https://server8.mp3quran.net/download/afs/{}.mp3",
    "2": "https://server11.mp3quran.net/download/shatri/{}.mp3",
    "3": "https://server6.mp3quran.net/download/qtm/{}.mp3",
}

makeDir("api")
makeDir("api/audio")
makeJson("api/reciters.json", reciters)

surahNames = readJsonFile("surah.json")
surahData = readJsonFile("surahData.json")
quranAr = readJsonFile("quran_ar.json")
quranEn = readJsonFile("quran_en.json")
quranBn = readJsonFile("quran_bn.json")


allSurahData = []


for surahNo in range(1, 115):
    eng = quranEn[surahNo - 1]
    ara = quranAr[surahNo - 1]
    ben = quranBn[surahNo - 1]

    totalAyah = len(eng)
    surahInfo = surahData[surahNo - 1]
    surahName = surahInfo["surahName"]
    surahNameAr = surahInfo["surahNameAr"]
    surahNameArLong = surahInfo["surahNameArLong"]
    surahNameTranslation = surahInfo["surahNameMeaning"]
    revelationPlace = surahInfo["revelationPlace"]
    verseAudio = "https://quranaudio.pages.dev/{num}/{surahNo}_{ayahNo}.mp3"
    chapterAudio = "https://github.com/falah-club/Quran-Audio/raw/refs/heads/main/Data/{}/{}.mp3"

    # Make the folder
    makeDir(f"api/{surahNo}")

    for ayahNo in range(1, totalAyah + 1):
        english = eng[ayahNo - 1]
        arabic1, arabic2 = ara[ayahNo - 1]
        bengali = ben[ayahNo - 1]

        ayahData = {
            "surahName": surahName,
            "surahNameArabic": surahNameAr,
            "surahNameArabicLong": surahNameArLong,
            "surahNameTranslation": surahNameTranslation,
            "revelationPlace": revelationPlace,
            "totalAyah": totalAyah,
            "surahNo": surahNo,
            "ayahNo": ayahNo,
            "english": english,
            "arabic1": arabic1,
            "arabic2": arabic2,
            "bengali": bengali,
            "audio": {
                i: {
                    "reciter": j,
                    "url": verseAudio.format(num=i, surahNo=surahNo, ayahNo=ayahNo),
                }
                for (i, j) in reciters.items()
            },
        }

        makeJson(f"api/{surahNo}/{ayahNo}.json", ayahData)

        print(f"Done {ayahNo} of {surahNo}\r", end="")

    finalData = {
        "surahName": surahName,
        "surahNameArabic": surahNameAr,
        "surahNameArabicLong": surahNameArLong,
        "surahNameTranslation": surahNameTranslation,
        "revelationPlace": revelationPlace,
        "totalAyah": totalAyah,
        "surahNo": surahNo,
        "audio": {
            i: {
                "reciter": j,
                "url": chapterAudio.format(i, surahNo),
                "originalUrl": originalUrl[i].format(f"{surahNo:03}"),
            }
            for (i, j) in reciters.items()
        },
        "english": [i for i in eng],
        "arabic1": [i[0] for i in ara],
        "arabic2": [i[1] for i in ara],
        "bengali": [i for i in ben],
    }

    chapterAudioData = {
        i: {
            "reciter": j,
            "url": chapterAudio.format(i, surahNo),
            "originalUrl": originalUrl[i].format(f"{surahNo:03}"),
        }
        for (i, j) in reciters.items()
    }
    makeJson(f"api/{surahNo}.json", finalData)
    makeJson(f"api/audio/{surahNo}.json", chapterAudioData)
    allSurahData.append(
        {
            "surahName": surahName,
            "surahNameArabic": surahNameAr,
            "surahNameArabicLong": surahNameArLong,
            "surahNameTranslation": surahNameTranslation,
            "revelationPlace": revelationPlace,
            "totalAyah": totalAyah,
        }
    )
    print()

makeJson("api/surah.json", allSurahData)


os.system("python generateSitemap.py")