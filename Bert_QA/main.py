import spacy
from sty import fg, bg, ef, rs
from question_processor import QuestionProcessor
from text_extractor import TextExtractor
from text_extractor_pipe import TextExtractorPipe
from context_retriever import ContextRetriever
from answer_retriever import AnswerRetriever
from find_keywords import FindKeywords

# STEP 1: Extract keywords from the question
print(fg.green + "Please enter your question here: " + fg.rs)
question = input()
getKeywords = FindKeywords(question)
key_word = getKeywords.distill()

# STEP 2: Download text from wikipedia
textExtractor = TextExtractor(key_word, "1")
textExtractor.extract()
textExtractorPipe = TextExtractorPipe()
textExtractorPipe.addTextExtractor(textExtractor)

# STEP 3: Retrieve corpus from the text.
nlp = spacy.load('en_core_web_sm')
nlp.add_pipe('sentencizer')
doc = nlp(textExtractorPipe.extract())
sentences = [sent.text.strip() for sent in doc.sents]
questionProcessor = QuestionProcessor(nlp)
contextRetriever = ContextRetriever(nlp, 3)
questionContext = contextRetriever.getContext(sentences, questionProcessor.process(question))

# STEP 4: Retrieve answer from the corpus.
answerRetriever = AnswerRetriever()
answerRetriever.getAnswer(question, questionContext)
