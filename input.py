def inpTxt(fileName):
  f = open(fileName)
  # The file format should be PMID\tAbstract_content\n for each entry
  newAbst_List = []
  pmid_List = [] #PMID can also be accession ID created by user
  for line in f:
    line = line.rstrip()
    if line:
      pmid_List.append(line.split("\t")[0])
      newAbst_List.append(line.split("\t")[1])
  f.close()
  # concatenate/zip resulted abstracts (or titles) with their respectative pmids
  ab_idDict = dict(zip(pmid_List, newAbst_List))
  return ab_idDict

def inpPMID(pmidList, userMail, saveAbst=True, saveAbst_fileName="Abstracts"):
    ### get abstracts for all pmids from user's input
  from Bio import Entrez
  import csv

  Entrez.email = userMail # userMail shoud be a string
  # get the abstracts (or titles if abstracts are not available)
  handle = Entrez.efetch(db="pubmed", id=pmidList, rettype="xml", retmode="text")
  record = Entrez.read(handle)
  abstr = []
  for pmArt in record["PubmedArticle"]:
      if 'Abstract' in pmArt['MedlineCitation']['Article'].keys():
          abstr.append(pmArt['MedlineCitation']['Article']["Abstract"]["AbstractText"][0])
      else:
          abstr.append(pmArt['MedlineCitation']['Article']["ArticleTitle"])

  # concatenate/zip resulted abstracts (or titles) with their respectative pmids
  ab_idDict = dict(zip(pmidList,abstr))
  
  # import the dict into a csv excel file if user chose to save (default)
  if saveAbst:
    with open(saveAbst_fileName+".csv", "w") as output:
        writer = csv.writer(output)
        writer.writerow(["pmID", "Abstract"])
        for k, v in ab_idDict.items():
            writer.writerow([k, v])
            
  return ab_idDict

def nerInput():

  option = int(input("""User can enter either a text file or PudMed IDs as input to retrieve abstract content.

  For the text file option, the file can contain 1 or multiple abstracts, 1 line for each abstract and the line should be formatted as tab separated values: PMID\tAbstract_content
  (with the PMID can be replaced with your own ordinary number or any accession ID of your choice).

  For the PudMed IDs option, besides a list of all pmids, user would need to provide their email address for retrieval of Medline contents via Entrez.
  The email address should be valid and entered as a string. 
  There are also options if user wants to save the retrieved results as a csv file or not; if yes, user can enter the file's name when directed.
  The default settings are to save the retrieved results under the name "Abstracts.csv".

  Type 1 if your input is TXT file; Type 2 if your input is PubMed ID: """))

  if option == 1:
    fileName = str(input("Please enter the name of your text file: "))
    ab_id = inpTxt(fileName)
  elif option == 2:  
    saveAbst = True; saveAbst_fileName = "Abstracts"
    pmidList = list(set(str(input("Please enter the list of all PubMed IDs, separated by comma and space (Example: 4329581, 32104937): ")).split(", ")))
    userMail = str(input("Please enter your email: "))
    saveOpt = str(input('Do you want all the retrieved abstract content to be save as a CSV file? Please enter "y", "yes", or "true" if you want to save: '))
    if saveOpt.lower() == "y" or saveOpt.lower() == "yes" or saveOpt.lower() == "true":
      saveAbst_fileName = str(input('Please enter the name of the csv file you wanted to save: '))
    else:
      saveAbst = False
    ab_id = inpPMID(pmidList, userMail, saveAbst, saveAbst_fileName)
  else:
    ab_id = dict()
    print("Your option was invalid! Please try again and enter either 1 or 2.")

  return ab_id