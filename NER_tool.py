from custom_tokenizer import customize_tokenizer
from input import nerInput
from output import nerOutput

# Input
ab_id = nerInput()

# Output
if len(ab_id) > 0:
  nerOutput(ab_id)
