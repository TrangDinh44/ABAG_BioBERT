
# Perform NER on abstract content
def modelNER(samples, modelDir):
  from simpletransformers.ner import NERModel

  # LOAD the newly trained bioBERT model
  model = NERModel('bert', modelDir, use_cuda=use_cuda)

  # Analyze the abstract using the model
  # tokenize abstract content
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
def predForm(predArr):
  token = [[] for i in range(len(predArr))]
  label = [[] for i in range(len(predArr))]

  for i in range(len(predArr)):
    for dic in predArr[i]:
      for k, v in dic.items():
        token[i].append(k)
        label[i].append(v)
  
  startAB = 0; startAG = 0; end = 0
  trueAb = []; trueAg = []
  for i in range(len(token)):
    if label[i] == 'B-Antibody':
      startAB = i
    elif label[i] == 'B-Antigen':
      startAG = i
    if label[i] != 'I-Antibody' and label[i] != 'I-Antigen':
      end = i
      if startAB != 0 and startAB < end:
        trueAb.append(" ".join(token[startAB:end]))
        startAB = 0; end = 0
      elif startAG != 0 and startAG < end:
        trueAg.append(" ".join(token[startAG:end]))
        startAG = 0; end = 0
  return trueAb, trueAg

# Post-processing the output
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
  if str(input('''Do you want to save the output results in a text file?
  Type "y", "yes", or "true" if you want to save: ''')).lower() not in posOpt:
    saveOut = False
    
  # Ask for user's GPU option
  use_cuda = False
  if str(input('''Are you using GPU?
  Type "y", "yes", or "true" if GPU is on: ''')).lower() in posOpt:
    use_cuda = True
  
  samples = [v for v in ab_id.values()]
  modelDir = str(input('Enter the directory where you put the model: '))
  predAbs, predAgs = predForm(modelNER(samples, modelDir))
  
  text = ""
  text += "//\nPMID: " + k + "\n"
  if abagOpt == 1 or abagOpt == 3:
    text += "Antibody names:\t" + ", ".join(predAbs) + "\n"
  if abagOpt == 2 or abagOpt == 3:
    text += "Antigen names:\t" + ", ".join(predAgs) + "\n"

  print(text)

  if saveOut:
    f = open("ABAG_NER_Results.txt", "w")
    f.write(text)
    f.close()
