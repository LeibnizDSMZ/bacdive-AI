import pickle
import os
import argparse
import numpy as np
import csv

# set up possible arguments
parser = argparse.ArgumentParser(description="BacDive-AI package",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("trait", help="Trait to predict, all to see all models")
parser.add_argument(
    "file", help="Interproscan file or file with list of Pfams")

# load configuration from command line arguments
args = parser.parse_args()
config = vars(args)

# define constants
EVALUE = 1e-20
MODELPATH = os.path.dirname(__file__)+"/models/"

# set up all available models
traits = {
    "acidophile": 'Acidophilic',
    "gram-positive": 'Gram-positive',
    "spore-forming": 'Spore-forming',
    "aerobic": 'Aerobic',
    "anaerobic": 'Anaerobic',
    "thermophile": 'Thermophilic',
    "psychrophile": 'Psychrophilic',
    "motile2+": 'Flagellated motility',
}

# check if selected trait is supported
trait = config.get('trait')
if trait != 'all' and trait not in traits:
    print(trait, 'is not supported')
    print('Supported traits are:', ', '.join(list(traits.keys())))
    exit()

# load pfam data set
pfams = []
filename = config.get('file')
with open(filename, 'r', encoding='utf-8') as f:
    csv_file = csv.reader(f, delimiter='\t')
    for line in csv_file:
        evalue = float(line[8])
        if evalue > EVALUE:
            continue
        pfams.append(line[4])
pfams = set(pfams)

# if specific trait has been selected, reduce to this
if trait != 'all': 
    traits = {trait: traits[trait]}

# go through all remaining traits
for trait in traits:
    label = traits[trait]

    # load model
    dump = pickle.load(open(MODELPATH + trait + "_data.p", "rb"))
    clf = dump.get('model')
    categories = dump.get("categories")
    strains = dump.get('strains')

    # transform sample
    lst = dict(zip(*np.unique(list(pfams), return_counts=True)))
    X = [lst.get(k) if k in lst else 0 for k in categories]

    # predict with probability
    proba = clf.predict_proba([X])
    y = proba.argmax(axis=1)
    y = y[0]
    proba = proba[0]
    true_index = list(clf.classes_).index(y)

    # print result
    result = f"{label}: {bool(y)} ({round(proba[true_index]*100, 2)}%)"
    print(result)
