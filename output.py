# Perform NER on all abstract content
def modelNER(samples, modelDir, useCuda, nerOut):
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
  
  if nerOut:
    for idx, sample in enumerate(samples):
      print("\n")
      print('Abstract #%d:' % (idx+1))    # print sentence number
      print(sample)
      for word in predictions[idx]:
        print('{}'.format(word))   # print the tokens and their labels
      
  return predictions

# Re-format the predicted results
def predForm(predArr, nameOnly):
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

    if nameOnly:
      trueAb[abstNo] = list(set(trueAb[abstNo]))
      trueAg[abstNo] = list(set(trueAg[abstNo]))

  return trueAb, trueAg

# Post-processing the output based on user's direction
def nerOutput(ab_id):
  posOpt = ["y", "yes", "true"]
  
  #Ask for user's output options
  abagOpt = int(input('''\nPlease choose the entity/entities for NER:
  Type 1 for AB only
  Type 2 for AG only
  Type 3 for both AB and AG
  Enter a number (1, 2, or 3): '''))
  
  nerOut = True
  if str(input('''Do you want name extraction only or NER visualization? 
  Type "y", "yes", or "true" if you want NER visualization: ''')).lower() not in posOpt:
    nerOut = False

  nameOnly = True
  if str(input('''Do you want the output results to include frequencies of name mentions?
  Type "y", "yes", or "true" if you want to include frequencies: ''')).lower() in posOpt:
    nameOnly = False
    
  saveOut = True
  if str(input('''Do you want to save the recognized names in a text file?
  Type "y", "yes", or "true" if you want to save: ''')).lower() not in posOpt:
    saveOut = False
    
  # Ask for user's GPU option
  useCuda = False
  if str(input('''Are you using GPU? GPU is recommended for speedy performance.
  Type "y", "yes", or "true" if GPU is on: ''')).lower() in posOpt:
    useCuda = True
  
  samples = [str(v) for v in ab_id.values()]
  modelDir = str(input('Enter the directory where you put the model: '))
  predAbs, predAgs = predForm(modelNER(samples, modelDir, useCuda, nerOut), nameOnly)
  
  pmIDs = [k for k in ab_id.keys()]
  text = ""

  for abstNo in range(len(ab_id)):
    text += "//\nPMID: " + pmIDs[abstNo] + "\n"
    if abagOpt == 1 or abagOpt == 3:
      text += "Antibody names:\t" + ", ".join(predAbs[abstNo]) + "\n"
    if abagOpt == 2 or abagOpt == 3:
      text += "Antigen names:\t" + ", ".join(predAgs[abstNo]) + "\n"

  print(text)

  if saveOut:
    f = open("ABAG_NER_Results.txt", "w")
    f.write(text)
    f.close()
