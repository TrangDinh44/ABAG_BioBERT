# ABAG_NER
NER Model for Antibody-Antigen entities, fine-tuned with pre-trained BioBERT

# Usage
This ABAG_NER package serves as a tool to automatically extract Antibody and/or Antigen names mentioned in PubMed abstracts or user-provided texts.

# Instructions
1. Clone the repository to your coding environment by typing the script: 

   !git clone https://github.com/TrangDinh44/ABAG_BioBERT.git
   
2. Set the working directory to the 'ABAG_BioBERT' folder, then install all the required packages listed in requirements.txt.

3. In this working directory, download our trained ABAG_NER model from https://drive.google.com/drive/folders/16nKwwyuWqMK7upiL4cR-W1jcB6TWeI0-?usp=sharing

4. Invoke the Simple Transformers:

!pip install -q simpletransformers

5. Run the script file NER_tool.py and follow instructions (printed on screen).
