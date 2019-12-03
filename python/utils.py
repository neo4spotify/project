import pandas as pd
import subprocess
import sys
from neo4j import GraphDatabase


def readHead(fileName, delimiter=";"):
    df = pd.read_csv(fileName, delimiter=delimiter, header=0)
    return df.head(3)

def pip_auto_install():
    """
    Automatically installs all requirements if pip is installed.
    """
    subprocess.call([sys.executable, "-m", "pip",
                     "install", "-r requirements.txt"])

if __name__ == "__main__":
    pip_auto_install()
    print("Imports réalisés")
