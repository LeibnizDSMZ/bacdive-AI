# BacDive AI models


This is a small command line tool bundled with selected BacDive-AI models to predict bacterial phenotypes from InterPro (Pfam) annotations. Please see the following Preprint for more information: https://doi.org/10.1101/2024.08.12.607695


## Installation instructions

This repository comes with zipped models because of their large file size. Please unzip the models into the `/models` path before using them.

Furthermore, the following requirements must be met:

- Python v3.9 or higher
- scikit-learn v1.4.0

This package comes with an example InterPro annotation of the strain [_Actinomyces dentalis_ DSM 19115](https://bacdive.dsmz.de/strain/189). The annotated file in TSV format is named as `1120941.3.faa.tsv`. The genome is derived from [BV-BRC](https://www.bv-brc.org/view/Genome/1120941.3) (formerly PATRIC).

For reference, the used command to generate the Pfams with [InterProScan](https://interproscan-docs.readthedocs.io/en/latest/) was:

```bash
interproscan.sh -i 1120941.3.faa -f tsv -d ./ -appl Pfam
```

To start the prediction of a single trait, you can use the following example code in the project folder:

```bash
python predict.py gram-positive 1120941.3.faa.tsv
```

For the aforementioned call, you can select one of the following values:

| Value         | Trait                |
| ------------- | -------------------- |
| acidophile    | Acidophilic          |
| gram-positive | Gram-positive        |
| spore-forming | Spore-forming        |
| aerobic       | Aerobic              |
| anaerobic     | Anaerobic            |
| thermophile   | Thermophilic         |
| psychrophile  | Psychrophilic        |
| motile2+      | Flagellated motility |

You can also choose `all` to see the complete list of predicted values:

```bash
python predict.py all 1120941.3.faa.tsv
```

You will get the prediction (true or false) for each of the trait together with a confidence score. The output should look like this:

```
Acidophilic: False (98.5%)
Gram-positive: True (98.93%)
Spore-forming: False (96.47%)
Aerobic: False (93.91%)
Anaerobic: True (63.54%)
Thermophilic: False (99.77%)
Psychrophilic: False (99.96%)
Flagellated motility: False (99.85%)
```
