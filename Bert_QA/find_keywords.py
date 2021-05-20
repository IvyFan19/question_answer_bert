
from sty import bg

class FindKeywords:
    __question: str

    def __init__(self, question):
        print("\n")
        print(bg.blue + "STEP 1: Extract keywords from the question" + bg.rs)
        self.__question = question

    def distill(self):
        if self.__question[-1] == "?":
             self.__question = self.__question[:len(self.__question)-1]
        
        sep_words = self.__question.split()
        print("The key word is: " + sep_words[-1])
        return sep_words[-1]
            

## Test distill function
# question = "How many states are in the USA?"
# getKeywords = FindKeywords(question)
# key_word = getKeywords.distill()
# print(key_word)
