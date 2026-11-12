# BIOT 6900 Module 9, Notebook 3: Clinical NLP and leakage

Name: Dhairya Bhatia

## What I did
I used the synthetic sepsis cohort (400 patients, 3 notes each, 23% died). The notebook pulls features out of the notes, trains a logistic regression to predict death, and checks which features the model relies on. Then I removed the features that are leakage and re-ran it.

## Results (5-fold cross-validated AUROC)
- All features: 0.939
- Declared leakage removed (pressors, intubation, comfort care): 0.839
- All leakage removed (also renal replacement): 0.769

## What I found
- The model looked very good at first (0.939), but part of that was leakage.
- Pressors, intubation, comfort care and renal replacement are things done to patients who are already getting worse. They show up in the final note, so they give away the outcome.
- After removing all four, the AUROC dropped to 0.769. About 39% of the model's skill above chance was leakage.
- 0.769 is decent but not great. It is the number I would trust, because it only uses things known early (age, lactate, lactate not clearing).
- Removing only my own leakage still left 0.839. That was the clue that a hidden leak (renal replacement) was still in there.

## What did not work
- My first leakage list missed renal replacement, so the score stayed too high until I found it.
- Only one cohort and one seed, and only about 90 deaths, so the numbers are noisy (the fold-to-fold spread was about 0.04).
- The data is synthetic and rule-generated, so real charts would be messier (documentation bias, copy-forward notes).
