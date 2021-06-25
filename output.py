def modelLoad(nameOnly):
  from simpletransformers.ner import NERModel

  # Ask for user's GPU option
  use_cuda = False
  if str(input("Use GPU?")) == "yes":
    use_cuda = True

  # LOAD the newly trained bioBERT model
  model = NERModel('bert', modelDir, use_cuda=use_cuda)

  # Analyze the abstract using the model
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

# Perform NER on abstract content
def modelAnalyze(abstCont):
  model = modelLoad()
  predAbs = []; predAgs = []
    
  #get lists of all predicted tags
  anaText = ' '.join([str(x) for x in custom_nlp(abstCont)])
  anaDict = model.analyze(anaText)
  for ent in anaDict['entities']:
    if ent['type'] == "Antibody":
      predAbs.append(ent['text'])
    else:
      predAgs.append(ent['text'])

  if nameOnly:
    predAbs = list(set(predAbs))
    predAgs = list(set(predAgs))
      
  return predAbs, predAgs

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
  if str(input('''Do you want to name extraction only or NER visualization? 
  Type "y", "yes", or "true" if you want NER visualization: ''')).lower() not in posOpt:
    nerOut = False

  saveOut = True
  if str(input('''Do you want to save the output results in a text file?
  Type "y", "yes", or "true" if you want to save: ''')).lower() not in posOpt:
    saveOut = False
  
  text = ""

  for k, v in ab_id.items():
    predAbs, predAgs = modelAnalyze(v)

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
