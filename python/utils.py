import pandas as pd
import subprocess
import sys
from neo4j import GraphDatabase
try:
    from pip import main as pipmain
except:
    from pip._internal.main import main as pipmain



def readHead(fileName, delimiter=";"):
    df = pd.read_csv(fileName, delimiter=delimiter, header=0)
    return df.head(3)


def pip_auto_install():
    """
    Automatically installs all requirements if pip is installed.
    """
    pipmain(['install', '-r', 'requirements.txt'])

if __name__ == "__main__":
    pip_auto_install()
    print("Imports réalisés")
