# Ask and classify user's options
def userOpt(question):
  posOpt = posOpt = ["y", "yes", "true"]
  return str(input("\n"+question)).lower() in posOpt

# Process user's print and/or save options
def outPrintSave(text, taskName):
  print("\n" + taskName + " has been completed!")
  if userOpt('Do you want to print out the results?\nType "y", "yes", or "true" if you want to print: '):
    print(text)
  if userOpt('Do you want to save the results in a text file?\nType "y", "yes", or "true" if you want to save: '):
    f = open(str(input("Enter the name you want to save the resulted file as: ")) +".txt", "w")
    f.write(text)
    f.close() 

# Perform NER on all abstract content
def modelNER(samples, modelDir, useCuda):
  from simpletransformers.ner import NERModel

  # LOAD the newly trained bioBERT model
  model = NERModel('bert', modelDir, use_cuda=useCuda)

  # Analyze the abstract using the model
  # tokenize abstract content
  import spacy
  from custom_tokenizer import customize_tokenizer
  # Create a customized tokenizer
  custom_nlp = spacy.load('en_core_web_sm')
  custom_nlp.tokenizer = customize_tokenizer(custom_nlp)
  samples = [' '.join([str(x) for x in custom_nlp(i)]) for i in samples]
  # model returns an array in the 'predictions' variable
  predictions, raw_outputs = model.predict(samples)
  
  if userOpt('Do you want name extraction only or NER visualization?\nType "y", "yes", or "true" if you want NER visualization: '):
    nerText = ""
    for idx, sample in enumerate(samples):
      nerText += "\nAbstract #%d:\n"%(idx+1) + sample + "\n" # print abstract number and content
      for word in predictions[idx]:
        nerText += '{}'.format(word) + "\n"   # print the tokens and their labels
    outPrintSave(nerText, "The NER visualization task")
      
  return predictions

# Re-format the predicted results
def predForm(predArr, allMent):
  token = [[] for i in range(len(predArr))]
  label = [[] for i in range(len(predArr))]

  for i in range(len(predArr)):
    for dic in predArr[i]:
      for k, v in dic.items():
        token[i].append(k)
        label[i].append(v)
  
  startAB = 0; startAG = 0; end = 0
  trueAb = [[] for i in range(len(token))]
  trueAg = [[] for i in range(len(token))]
  for abstNo in range(len(token)):
    for i in range(len(token[abstNo])):
      if label[abstNo][i] == 'B-Antibody':
        startAB = i
      elif label[abstNo][i] == 'B-Antigen':
        startAG = i
      if label[abstNo][i] != 'I-Antibody' and label[abstNo][i] != 'I-Antigen':
        end = i
        if startAB != 0 and startAB < end:
          trueAb[abstNo].append(" ".join(token[abstNo][startAB:end]))
          startAB = 0; end = 0
        elif startAG != 0 and startAG < end:
          trueAg[abstNo].append(" ".join(token[abstNo][startAG:end]))
          startAG = 0; end = 0

    if not allMent:
      trueAb[abstNo] = list(set(trueAb[abstNo]))
      trueAg[abstNo] = list(set(trueAg[abstNo]))

  return trueAb, trueAg

# Post-processing the output based on user's direction
def nerOutput(ab_id):
  posOpt = ["y", "yes", "true"]
  
  #Ask for user's output options
  try:
    abagOpt = int(input('''\nPlease choose the entity/entities for NER:
    Type 1 for AB only
    Type 2 for AG only
    Type 3 for both AB and AG
    Enter a number (1, 2, or 3): '''))
  except ValueError:
    return "Your option is INVALID! Please try again and enter 1, 2, or 3 as an INTEGER."

  allMent = userOpt('''The same ABAG names may appear multiple times in an abstract.
  Do you want the output results to list all such mentions or just unique names?
  Type "y", "yes", or "true" if you want to list all mentions: ''')
  useCuda = userOpt('Are you using GPU? GPU is recommended for speedy performance.\nType "y", "yes", or "true" if GPU is on: ')
  
  samples = [str(v) for v in ab_id.values()]
  modelDir = str(input('\nEnter the directory where you put the model: '))
  predAbs, predAgs = predForm(modelNER(samples, modelDir, useCuda), allMent)
  
  pmIDs = [k for k in ab_id.keys()]
  text = "\n"

  for abstNo in range(len(ab_id)):
    text += "//\nPMID: " + pmIDs[abstNo] + "\n"
    if abagOpt == 1 or abagOpt == 3:
      text += "Antibody names:\t" + ", ".join(predAbs[abstNo]) + "\n"
    if abagOpt == 2 or abagOpt == 3:
      text += "Antigen names:\t" + ", ".join(predAgs[abstNo]) + "\n"
  
  outPrintSave(text, "The name extraction task")
