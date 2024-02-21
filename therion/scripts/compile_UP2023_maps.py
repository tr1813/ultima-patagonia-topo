#%%
import subprocess
import os
#%%

BASENAMES_106 = ["AvenDesArchesPerdues", 
             "CuevaNoTime",
             "CuevaPirates", 
             "GouffreDejaVu", 
             "GouffreDuBowling",
             "GouffrePlusPlus", 
             "GrandeFailleDuBoutDuMonde",
             "Perte25MetresNageLibre",
             "PerteChampis",
             "PorcheEden",
             "PuitsDeLArche",
             "ReveEveille",
             "TraverseeDeLIndecision"
             ]

BASENAMES_107 = ["GrotteDeLAncien"]
BASENAMES_403 = ["GrotteLapisLazuli"]
BASENAMES_402 = ["Perte3-HPS35","Perte5-HPS35","Perte7-HPS35","MoulinDeLaScience"]
# %%

path_to = os.path.normpath('../data/106/')
os.chdir(path_to)

for name in BASENAMES_106:
    print(os.getcwd())

    print(f"compiling the maps for cave {name}")
    os.chdir(name)
    subprocess.check_output("therion config.thconfig", shell=True)
    os.chdir("..")


# %%
path_to = os.path.normpath('../107')
os.chdir(path_to)

for name in BASENAMES_107:
    print(os.getcwd())
    print(f"compiling the maps for cave {name}")

    os.chdir(name)
    subprocess.check_output("therion config.thconfig", shell=True)
    os.chdir("..")
    
# %%
path_to = os.path.normpath('../402')
os.chdir(path_to)

for name in BASENAMES_402:
    print(os.getcwd())
    os.chdir(name)
    subprocess.check_output("therion config.thconfig", shell=True)
    os.chdir("..")


# %%
path_to = os.path.normpath('../403')
os.chdir(path_to)

for name in BASENAMES_403:
    print(os.getcwd())
    os.chdir(name)
    subprocess.check_output("therion config.thconfig", shell=True)
    os.chdir("..")