from custom_tokenizer import customize_tokenizer
from input import nerInput
from output import nerOutput

import spacy
# Create a customized tokenizer
custom_nlp = spacy.load('en_core_web_sm')
custom_nlp.tokenizer = customize_tokenizer(custom_nlp)

# Input
ab_id = nerInput()

# Output
if len(ab_id) > 0:
  nerOutput(ab_id)
