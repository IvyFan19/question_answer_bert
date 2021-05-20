import wikipedia
import os
from sty import fg, bg, ef, rs

class TextExtractor:
    __pageTitle: str
    __pageId: str

    def __init__(self, pageTitle, pageId):
        print("\n")
        print(bg.blue + "STEP 2: Download content from Wikipedia"+ bg.rs)
        self.__pageTitle = pageTitle
        self.__pageId = pageId

    def extract(self):
        fileName = "./text/" + self.__pageTitle + ".txt"
        if not os.path.isfile(fileName):
            page = wikipedia.page(title=self.__pageTitle, pageid=self.__pageId)
            f = open(fileName, "w")
            f.write(page.content)
            f.close()
        print("The wiki content has been saved in " + self.__pageTitle + ".txt" )

    def getText(self):
        f = open("./text/" + self.__pageTitle + ".txt", "r")
        return f.read()
