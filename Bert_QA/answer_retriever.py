
import torch
from transformers import BertForQuestionAnswering
from colorama import Style
from colorama import Fore
from transformers import BertTokenizer
import textwrap
from sty import bg

class AnswerRetriever:
    def getAnswer(self, question, questionContext):
        print("\n")
        print(bg.blue + "STEP 4: Retrieve answer by Bert"+ bg.rs)

        model = BertForQuestionAnswering.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
        
        tokenizer = BertTokenizer.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')

        # Wrap text to 80 characters.
        wrapper = textwrap.TextWrapper(width=80) 
        
        show_question = Fore.GREEN + "Question: " + Style.RESET_ALL
        print(show_question + question)

        answer_text = questionContext
        # ====== Wrap answer_text to 80 characters =======
        answer_text = wrapper.fill(answer_text)

        # ======== Tokenize ========
        # Apply the tokenizer to the input text, treating them as a text-pair.
        input_ids = tokenizer.encode(question, answer_text)

        # Report how long the input sequence is.
        # print('Query has {:,} tokens.\n'.format(len(input_ids)))

        # ======== Set Segment IDs ========
        # Search the input_ids for the first instance of the `[SEP]` token.
        sep_index = input_ids.index(tokenizer.sep_token_id)

        # The number of segment A tokens includes the [SEP] token istelf.
        num_seg_a = sep_index + 1

        # The remainder are segment B.
        num_seg_b = len(input_ids) - num_seg_a

        # Construct the list of 0s and 1s.
        segment_ids = [0]*num_seg_a + [1]*num_seg_b

        # There should be a segment_id for every input token.
        assert len(segment_ids) == len(input_ids)

        # ======== Evaluate ========
        # Run our example through the model.
        outputs = model(torch.tensor([input_ids]), # The tokens representing our input text.
                        token_type_ids=torch.tensor([segment_ids]), # The segment IDs to differentiate question from answer_text
                        return_dict=True) 

        start_scores = outputs.start_logits
        end_scores = outputs.end_logits

        # ======== Reconstruct Answer ========
        # Find the tokens with the highest `start` and `end` scores.
        answer_start = torch.argmax(start_scores)
        answer_end = torch.argmax(end_scores)

        # Get the string versions of the input tokens.
        tokens = tokenizer.convert_ids_to_tokens(input_ids)

        # Start with the first token.
        answer = tokens[answer_start]

        # Select the remaining answer tokens and join them with whitespace.
        for i in range(answer_start + 1, answer_end + 1):
            
            # If it's a subword token, then recombine it with the previous token.
            if tokens[i][0:2] == '##':
                answer += tokens[i][2:]
            
            # Otherwise, add a space then the token.
            else:
                answer += ' ' + tokens[i]

        show_ans = Fore.GREEN + "Answer: " + Style.RESET_ALL
        print(show_ans + answer)

# example = AnswerRetriever() 
# question = "Where is the capital city of Romania?"
# questionContext = "after World War I , Bucharest become the capital of Greater Romania .in 1862 , after Wallachia and Moldavia be unite to form the principality of Romania , Bucharest become the new nation 's capital city .capital city = = =it become the capital of Romania in 1862 and be the centre of romanian medium , culture , and art .economically , Bucharest be the most prosperous city in Romania .after the establishment of communism in Romania , the city continue grow .London be the capital and large city of England and the United Kingdom .be the capital and large city of Germany by both area and population .like all other local council in Romania , the Bucharest sectoral council , the capital 's general council , and the mayor be elect every four year by the population .history = = Bucharest 's history alternate period of development and decline from the early settlement in antiquity until its consolidation as the national capital of Romania late in the 19th century ."
# ans = example.getAnswer(question, questionContext)