from gensim.summarization.bm25 import BM25
from sty import fg, bg, ef, rs

class ContextRetriever:

    def __init__(self, nlp, numberOfResults):
        print("\n")
        print(bg.blue + "STEP 3: Retrieve corpus from the text"+ bg.rs)
        self.nlp = nlp
        self.numberOfResults = numberOfResults

    def tokenize(self, sentence):
        return [token.lemma_ for token in self.nlp(sentence)]

    def getContext(self, sentences, question):
        documents = []
        for sent in sentences:
            documents.append(self.tokenize(sent))

        bm25 = BM25(documents)

        scores = bm25.get_scores(self.tokenize(question))
        results = {}
        for index, score in enumerate(scores):
            results[index] = score

        sorted_results = {k: v for k, v in sorted(results.items(), key=lambda item: item[1], reverse=True)}
        results_list = list(sorted_results.keys())
        final_results = results_list if len(results_list) < self.numberOfResults else results_list[:self.numberOfResults]
        questionContext = ""
        for final_result in final_results:
            questionContext = questionContext + " ".join(documents[final_result])
        
        print(questionContext)
        return questionContext