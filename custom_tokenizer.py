import spacy
from spacy.tokenizer import Tokenizer
import re

def customize_tokenizer(nlp):  
  prefix_re = spacy.util.compile_prefix_regex(custom_nlp.Defaults.prefixes)
  suffix_re = spacy.util.compile_suffix_regex(custom_nlp.Defaults.suffixes)
  infix_re = re.compile(r'[]~/:+()\'[",_.>*•#-]')

  # Adds support to use special characters listed above as the delimiter for tokenization
  return Tokenizer(nlp.vocab, prefix_search=prefix_re.search,
                   suffix_search=suffix_re.search,
                   infix_finditer=infix_re.finditer,
                   token_match=None)

# Use 2-line script below to call the customize_tokenizer function:
#custom_nlp = spacy.load('en_core_web_sm')
#custom_nlp.tokenizer = customize_tokenizer(custom_nlp)
