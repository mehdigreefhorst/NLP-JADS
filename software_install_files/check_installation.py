import gensim
import numpy
import pandas
import matplotlib
import nltk
import sklearn

versions = ["4.3.3", "1.26.4", "2.2.2", "3.9.2", "3.9.1", "1.5.1"]

for package, version in zip([gensim, numpy, pandas, matplotlib, nltk, sklearn], versions):
    if package.__version__ != version:
        raise Exception(f"Version mismatch: {package.__name__} has version {package.__version__} but should be version {version}")
print("Congratulations! All versions are correct.")