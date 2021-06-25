import spacy
from spacy.tokenizer import Tokenizer
import re

def customize_tokenizer(nlp):
  custom_nlp = spacy.load('en_core_web_sm')
  prefix_re = spacy.util.compile_prefix_regex(custom_nlp.Defaults.prefixes)
  suffix_re = spacy.util.compile_suffix_regex(custom_nlp.Defaults.suffixes)
  infix_re = re.compile(r'[]~/:+()\\\'[",_.<>*•#-]')

  # Adds support to use special characters listed above as the delimiter for tokenization
  return Tokenizer(nlp.vocab, prefix_search=prefix_re.search,
                   suffix_search=suffix_re.search,
                   infix_finditer=infix_re.finditer,
                   token_match=None)
