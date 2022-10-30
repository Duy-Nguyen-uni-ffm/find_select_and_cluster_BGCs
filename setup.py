''' This setup file is used to (1) create a Python virtual environment, then (2) install or update two important tools: curl and Docker (which are used for installation and running of antiSMASH and BiGSCAPE).
    Then, (3) this file checks if the required programs, antiSMASH and BiGSCAPE, are already installed in defined directory "thirdparty_programs".
    It either then installs the programs, or skips if the programs are already preinstalled in defined location. This setup file is highly recommended to run in case the required programs are not preinstalled or installed in different locations. '''

# Run this file (highly recommended at first time setting up the pipeline or when the required programs are not installed in defined location) simply with python, e.g.: python3 set_up.py


import os


# Define control variables (assume required programs are not preinstalled in defined location):
found_antismash = False
found_bigscape  = False


# # -----------Preliminary setup-----------
print(">>> Creating a Python virtual environment... \n\n\n")
# Create and activate a Python virtual environment (recommended):
os.system("sudo apt install python3-virtualenv") # Install tool for creating virtual environment (if not available).
os.system("virtualenv -p $(which python3) ./thirdparty_programs/asenv")
os.system("source ./thirdparty_programs/asenv/bin/activate")
print("\n\n\n>>> Created a Python virtual environment!")

print("\n\n\n>>> Installing and updating required tools: curl and Docker... \n\n\n")
# Install/Update command "curl" (for installation of docker, then antiSMASH and BiGSCAPE):
os.system("which curl")
os.system("sudo apt-get update") # For this and the next codes, user password might be required!
os.system("sudo apt-get install curl")
# Install/Update Docker (to run antiSMASH and BiGSCAPE after installation):
os.system("curl -fsSL https://get.docker.com/ | sh")
os.system("sudo apt-get install docker.io")
print("\n\n\n>>> Installed and updated required tools!")

# print("\n\n\n>>> Installing and updating required Python libraries... \n\n\n")
# # Install/Update a few required Python libraries, if not yet available:
# os.system("source ./thirdparty_programs/asenv/bin/activate") # Activate virtual environment (again) so that the libraries will be installed to directory of virtual environment.
# os.system("pip install tabulate")
# os.system("pip install pandas")
# os.system("pip install matplotlib")
# print("\n\n\n>>> Installed and updated required Python libraries!")
# # -----------Preliminary setup-----------


current_dir = os.getcwd() # This should be path of common directory that contains all folders and scripts, including this one.


# # -----------antiSMASH-----------
# Check if running file of antiSMASH is already installed in defined location:
print("\n\n\n>>> Searching for running file of antiSMASH in defined location... ")
defined_path_of_antismash_runfile = current_dir + "/thirdparty_programs/run_antismash"
if os.path.isfile(defined_path_of_antismash_runfile):
    found_antismash = True # Assume in this case antiSMASH already properly installed in defined location.

# Install antiSMASH, or skip to next step:
if found_antismash == True:
    answer = input("\n\n\n>>> Found antiSMASH in defined location! Install antiSMASH again anyway (1) or skip to next step (2)? [1, 2] ").strip()
    while answer not in ["1", "2"]:
        answer = input(">>> Please input answer again: [1, 2] ").strip()
    if answer == "1":
        print("\n\n\n>>> Installing antiSMASH again (version 6.0.0)... (Warning: user password might be needed to run installation!)\n\n\n")
        if not os.path.isdir(current_dir + "/thirdparty_programs"):
            os.system("mkdir ./thirdparty_programs") # Create directory for containing antiSMASH if not exists already.
        os.system("curl -q https://dl.secondarymetabolites.org/releases/latest/docker-run_antismash-full > ./thirdparty_programs/run_antismash")
        os.system("chmod a+x ./thirdparty_programs/run_antismash")
        print("\n\n\n>>> Installed antiSMASH!")
    else:
        pass
else:
    print("\n\n\n>>> Cannot find antiSMASH in defined location. Installing antiSMASH (version 6.0.0)... (Warning: user password might be needed to run installation!)\n\n\n")
    if not os.path.isdir(current_dir + "/thirdparty_programs"):
        os.system("mkdir ./thirdparty_programs") # Create directory for containing antiSMASH if not exists already.
    os.system("curl -q https://dl.secondarymetabolites.org/releases/latest/docker-run_antismash-full > ./thirdparty_programs/run_antismash")
    os.system("chmod a+x ./thirdparty_programs/run_antismash")
    print("\n\n\n>>> Installed antiSMASH!")
# # -----------antiSMASH-----------


# # -----------BiGSCAPE-----------
# Check if running file of BiGSCAPE is already installed in defined location:
print("\n\n\n>>> Searching for running file of BiG-SCAPE CORASON in defined location... ")
defined_path_of_bigscape_runfile = current_dir + "/thirdparty_programs/run_bigscape"
if os.path.isfile(defined_path_of_bigscape_runfile):
    found_bigscape = True # Assume in this case BiGSCAPE already properly installed in defined location.

# Install BiGSCAPE, or skip this step:
if found_bigscape == True:
    answer = input(">>> Found BiG-SCAPE CORASON in defined location! Install BiG-SCAPE CORASON again anyway (1) or skip this step (2)? [1, 2] ").strip()
    while answer not in ["1", "2"]:
        answer = input(">>> Please input answer again: [1, 2] ").strip()
    if answer == "1":
        print("\n\n\n>>> Installing BiG-SCAPE CORASON again... (Warning: user password might be needed to run installation!)\n\n\n")
        if not os.path.isdir(current_dir + "/thirdparty_programs"):
            os.system("mkdir ./thirdparty_programs") # Create directory for containing BiGSCAPE if not exists already.
        os.system("curl -q https://git.wageningenur.nl/medema-group/BiG-SCAPE/raw/master/run_bigscape > ./thirdparty_programs/run_bigscape")
        os.system("chmod a+x ./thirdparty_programs/run_bigscape")
        print("\n\n\n>>> Installed BiG-SCAPE CORASON!")
    else:
        pass
else:
    print("\n\n\n>>> Cannot find BiG-SCAPE CORASON in defined location. Installing BiG-SCAPE CORASON... (Warning: user password might be needed to run installation!)\n\n\n")
    if not os.path.isdir(current_dir + "/thirdparty_programs"):
        os.system("mkdir ./thirdparty_programs") # Create directory for containing BiGSCAPE if not exists already.
    os.system("curl -q https://git.wageningenur.nl/medema-group/BiG-SCAPE/raw/master/run_bigscape > ./thirdparty_programs/run_bigscape")
    os.system("chmod a+x ./thirdparty_programs/run_bigscape")
    print("\n\n\n>>> Installed BiG-SCAPE CORASON!")
# # -----------BiGSCAPE-----------
