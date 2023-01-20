''' This setup file is used to (1) install or update two required tools: curl and docker (which are needed for the installation and running of antiSMASH and BiGSCAPE), 
    then (2) check if the required third-party programs, i.e. antiSMASH and BiGSCAPE, are already installed in the designated directory "thirdparty_programs",
    then either install the programs, or skip if the programs are already preinstalled in the designated location. This setup file is highly recommended to run in case the required programs are not preinstalled or were installed in other locations. '''

# This setup file can simply be run with python, e.g.: python3 setup.py


import os


# Define control variables (assume required programs are not preinstalled in the designated location):
found_antismash = False
found_bigscape  = False


# # -----------Preliminary setup: installation/update of curl and docker-----------
print("\n\n\n>>> Installing and updating required tools: curl and docker... \n\n\n")

# Install/Update command curl (needed for subsequent installation of docker, and antiSMASH as well as BiGSCAPE):
os.system("which curl")
os.system("sudo apt-get update") # For this and the next codes, user password might be asked!
os.system("sudo apt-get install curl")

# Install/Update docker (to run antiSMASH and BiGSCAPE after their installation):
os.system("curl -fsSL https://get.docker.com/ | sh")
os.system("sudo apt-get install docker.io")

print("\n\n\n>>> Installed and updated required tools!")
# # -----------Preliminary setup: installation/update of curl and docker-----------


current_dir = os.getcwd() # This should be path of common directory that contains all folders and files of the pipeline, including this setup file.


# # -----------Installation of antiSMASH-----------
# Check if running file of antiSMASH is already installed in designated location:
print("\n\n\n>>> Searching for running file of antiSMASH in designated location... ")
designated_path_of_antismash_runfile = current_dir + "/thirdparty_programs/run_antismash"
if os.path.isfile(designated_path_of_antismash_runfile):
    found_antismash = True # Assume in this case antiSMASH already properly installed in designated location.

# Install antiSMASH, or skip to next step:
if found_antismash == True:
    answer = input("\n\n\n>>> Found antiSMASH in designated location! Install antiSMASH again anyway (1) or skip to next step (2)? [1, 2] ").strip()
    while answer not in ["1", "2"]:
        answer = input(">>> Please input answer again: [1, 2] ").strip()
    if answer == "1":
        print("\n\n\n>>> Installing antiSMASH again... (Warning: user password might be asked during installation!)\n\n\n")
        if not os.path.isdir(current_dir + "/thirdparty_programs"):
            os.system("mkdir ./thirdparty_programs") # Create directory for antiSMASH if not exists already (this directory should already exist in this case, but just for safety).
        os.system("curl -q https://dl.secondarymetabolites.org/releases/latest/docker-run_antismash-full > ./thirdparty_programs/run_antismash")
        os.system("chmod a+x ./thirdparty_programs/run_antismash")
        print("\n\n\n>>> Installed antiSMASH!")
    else:
        pass
else:
    print("\n\n\n>>> Cannot find antiSMASH in designated location. Installing antiSMASH... (Warning: user password might be asked during installation!)\n\n\n")
    if not os.path.isdir(current_dir + "/thirdparty_programs"):
        os.system("mkdir ./thirdparty_programs") # Create directory for antiSMASH if not exists already.
    os.system("curl -q https://dl.secondarymetabolites.org/releases/latest/docker-run_antismash-full > ./thirdparty_programs/run_antismash")
    os.system("chmod a+x ./thirdparty_programs/run_antismash")
    print("\n\n\n>>> Installed antiSMASH!")
# # -----------Installation of antiSMASH-----------


# # -----------Installation of BiGSCAPE-----------
# Check if running file of BiGSCAPE is already installed in designated location:
print("\n\n\n>>> Searching for running file of BiG-SCAPE CORASON in designated location... ")
designated_path_of_bigscape_runfile = current_dir + "/thirdparty_programs/run_bigscape"
if os.path.isfile(designated_path_of_bigscape_runfile):
    found_bigscape = True # Assume in this case BiGSCAPE already properly installed in designated location.

# Install BiGSCAPE, or skip this step:
if found_bigscape == True:
    answer = input(">>> Found BiG-SCAPE CORASON in designated location! Install BiG-SCAPE CORASON again anyway (1) or skip this step (2)? [1, 2] ").strip()
    while answer not in ["1", "2"]:
        answer = input(">>> Please input answer again: [1, 2] ").strip()
    if answer == "1":
        print("\n\n\n>>> Installing BiG-SCAPE CORASON again... (Warning: user password might be asked during installation!)\n\n\n")
        if not os.path.isdir(current_dir + "/thirdparty_programs"):
            os.system("mkdir ./thirdparty_programs") # Create directory for BiGSCAPE if not exists already (this directory should already exist in this case, but just for safety).
        os.system("curl -q https://git.wageningenur.nl/medema-group/BiG-SCAPE/raw/master/run_bigscape > ./thirdparty_programs/run_bigscape")
        os.system("chmod a+x ./thirdparty_programs/run_bigscape")
        print("\n\n\n>>> Installed BiG-SCAPE CORASON!")
    else:
        pass
else:
    print("\n\n\n>>> Cannot find BiG-SCAPE CORASON in designated location. Installing BiG-SCAPE CORASON... (Warning: user password might be asked during installation!)\n\n\n")
    if not os.path.isdir(current_dir + "/thirdparty_programs"):
        os.system("mkdir ./thirdparty_programs") # Create directory for containing BiGSCAPE if not exists already.
    os.system("curl -q https://git.wageningenur.nl/medema-group/BiG-SCAPE/raw/master/run_bigscape > ./thirdparty_programs/run_bigscape")
    os.system("chmod a+x ./thirdparty_programs/run_bigscape")
    print("\n\n\n>>> Installed BiG-SCAPE CORASON!")
# # -----------Installation of BiGSCAPE-----------
