# BIOT 6900 Module 9, Notebook 3: Clinical NLP and leakage

Name: Dhairya Bhatia

Note: Sorry I ran the sepsis one earlier to test it out first before working on the HIV one.

## What I did
I used a synthetic HIV cohort (advanced immunosuppression, inpatient death as the outcome; 400 patients, 3 notes each, 25% died). The seed is my student ID. The notebook pulls features out of the notes, trains a logistic regression to predict death, and checks which features the model relies on. Then I removed the features that are leakage and re-ran it.

## Results (5-fold cross-validated AUROC)
- All features: 0.910
- Declared leakage removed (intubation, pressors, comfort care): 0.802
- All leakage removed (also renal replacement): 0.712

## What I found
- The model looked very good at first (0.910), but a lot of that was leakage.
- Comfort care, pressors, intubation and renal replacement are things done to patients who are already getting worse. They show up in the final note, so they give away the outcome.
- After removing all four, the AUROC dropped to 0.712. About 48% of the model's skill above chance was leakage.
- 0.712 is okay but not great. It is the number I would trust, because it only uses things known early (mainly lactate and age).
- Removing only my own leakage still left 0.802. That was the clue that a hidden leak (renal replacement) was still in there.

## What did not work
- My first leakage list missed renal replacement, so the score stayed too high until I found it.
- My own HIV signals (low CD4, PCP, ART nonadherence) barely mattered to the model (importance near zero), even though they are real risk factors.
- Only one cohort and one seed, and only about 100 deaths, so the numbers are noisy (the fold-to-fold spread was up to about 0.1).
- The data is synthetic and rule-generated, so real charts would be messier (documentation bias, copy-forward notes).
