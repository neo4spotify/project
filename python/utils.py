import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from neo4j import GraphDatabase
import squarify


def readHead(fileName, delimiter=";"):
    df = pd.read_csv(fileName, delimiter=delimiter, header=0)
    return df.head(3)



if __name__ == "__main__":
    print("Imports réalisés")
