def modelLoad():
  import anago

  # Retrive model
  print('Loading the trained NER model...')
  return anago.Sequence.load('weights_CV.h5', 'params_CV.json', 'preprocessor_CV.pkl')

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
  #Ask for user's output options
  abagOpt = int(input('''\nPlease choose the entity/entities for NER:
  Type 1 for AB only
  Type 2 for AG only
  Type 3 for both AB and AG
  Enter a number (1, 2, or 3): '''))
  nameOnly = True
  saveOut = True
  saveOpt = str(input('Do you want to save the output results in a text file? Type "y", "yes", or "true" if you want to save: '))
  if not (saveOpt == "y" or saveOpt == "yes" or saveOpt == "true"):
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
