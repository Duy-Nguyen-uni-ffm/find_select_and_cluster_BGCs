INSTRUCTIONS FOR SETUP AND RUNNING THE BIOINFORMATIC PIPELINE

>>> Short description of the bioinformatic pipeline:

> FUNCTION: This pipeline is developed to (1) find biosynthetic gene clusters (BGCs) on all DNA sequences given in FASTA file(s), (2) select from all identified BGCs the ones that can be considered complete and functional BGCs, and (3) analyze the similarity between the selected BGCs and the well-known BGCs from the database MIBiG.
> INPUT:    One or many FASTA files. These files need to be located (anywhere) inside the designated input directory (which is "input_for_antiSMASH").
> OUTPUT:   Output of all three mentioned tasks can be found in the designated directories (which are "output_from_antiSMASH", "selected_BGCs", "statistics" and "output_from_BiGSCAPE").

________________________________________________________________________________________________________________________


SYSTEM REQUIREMENTS (IMPORTANT)

>>> This pipeline should be operated on a Linux system. If not available on local computer, a virtual Linux system can be downloaded from the provider Oracle VM VirtualBox (specifically the package "VirtualBox-6.1.40-154048-Win" via link https://download.virtualbox.org/virtualbox/6.1.40/ together with the extension package "Oracle_VM_VirtualBox_Extension_Pack-6.1.16" via link https://www.virtualbox.org/wiki/Download_Old_Builds_6_1 and the (recommended) graphical package "kali-linux-2022.4-installer-amd64" via link https://www.kali.org/get-kali/), and set up on local computer (host system, e.g. Windows, will not be removed by the process) (setup of the virtual system takes about 30 minutes).

>>> This pipeline requires approx. 17 Gb on hard disk for setup and at least 2 CPUs and 2 Gb on RAM for an efficient operation.

________________________________________________________________________________________________________________________


SETUP (IMPORTANT)

>>> Command for creating a Python virtual environment, installing two utility tools (curl and docker), and the two required third-party programs, antiSMASH and BiG-SCAPE CORASON, to defined directory "thirdparty_programs" (if the two programs not preinstalled on local computer or installed in different locations):

> Run all-in-one setup file "setup.py" with Python, e.g. by typing in Terminal (opened in common directory, that is, directory that contains all files of pipeline):
python3 setup.py
> Note: A different running command to run setup file can be used (e.g. python). First time setup will take about 5 minutes. An internet connection is needed for this setup. During setup, certain input from user will be prompted e.g. user password, confirmation to download certain packages.

> Then activate the created Python virtual environment and install to this environment the following Python libraries (highly recommended, even if already available):
source ./thirdparty_programs/asenv/bin/activate
pip install tabulate
pip install pandas
pip install matplotlib

________________________________________________________________________________________________________________________


RUN (IMPORTANT)

>>> Commands for running pipeline (only after running setup or if required programs already preinstalled in defined location):

> Move input files into input directory for pipeline. There is no specific position for these files, i.e. the input files can be placed anywhere inside the input directory (they can all be found by the pipeline).
> Change execution right of running script, then run the pipeline by typing in Terminal (also in common directory):
chmod +x run_pipeline
sudo ./run_pipeline
> Note: This pipeline must be executed as root, therefore user login password is needed at the beginning to run pipeline! Password will then not be asked again while pipeline is running. At first time run of pipeline for task 1 and/or 3, certain large-sized packages might be installed by docker to run antiSMASH and BiG-SCAPE CORASON. This only happens at first run of pipeline, and will take about 40 minutes. In next runs, these will not be installed again.

________________________________________________________________________________________________________________________


>>> Further information to setting up and running this pipeline:

> For manual installation of antiSMASH: https://docs.antismash.secondarymetabolites.org/install/
> For manual installation of BiG-SCAPE CORASON: https://bigscape-corason.secondarymetabolites.org/installation/index.html
> Minimum requirements: This pipeline should be executed by Terminal on a UNIX operating system (e.g. Linux) with Python (version > 3.9).
> In order to execute task 1 (finding BGCs by antiSMASH) and task 3 (clustering of similar BGCs by BiG-SCAPE CORASON) with this pipeline, installation of the programs antiSMASH and BiG-SCAPE CORASON to the directory "thirdparty_programs" is required.
> In task 2 of this pipeline (i.e. BGC-selection), Genbank files created by antiSMASH can be processed. External Genbank files created by other software or for other purposes might not be compatible for task 2 of pipeline.
> A scheme for the workflow of this pipeline as well as for the BGC-selection algorithm can be found in the directory "info".
> This pipeline can only detect and analyze biosynthetic gene clusters (BGCs) encoding polyketides, peptides, terpenes, etc. that can be found on bacterial genomes (for finding BGCs on fungal or plant genomes, the option "--genefinding-tool" in file "run_antismash.py" must be adjusted).
> An internet connection for the computer executing the pipeline is recommended, although not necessarily needed for the execution of task 1, 2 and 3 of the pipeline, to allow the pipeline to access to the latest databases.

________________________________________________________________________________________________________________________


>>> Notes/tips:

>> General notes:
> Each of the executable task in this pipeline can be executed independently (i.e. this pipeline does not have to necessarily start with task 1 by every run), provided that the required input data (e.g. as zipped files/folders or unzipped files) are given in the corresponding input directory for the task.
> If a Python library needed for the execution of the pipeline is not yet installed on local computer (e.g. pandas), this can be installed by typing the command: "pip install <NAME OF LIBRARY>".
> The module "side_options.py" contains all options that can be adjusted for a customized usage of the pipeline, e.g. option to use predefined values for parameters so there is no need to input values for these parameters by every run.
> Output directories of all tasks can be emptied before executing task by adjusting the corresponding options in module "side_options.py". All files and folders in input directory for task 1 (gene prediction by antiSMASH) however will never be removed.

>> Task 1 (gene finding by antiSMASH):
> This pipeline can only analyze in this task FASTA files. These files will be searched in all locations of designated input directory.
> The results of gene detection can be viewed in HTML-format by clicking on the "index.html" file, which is located in the output directory.

>> Task 2 (BGC-selection):
> This pipeline searches and analyzes in this task Genbank (.gbk) files generated by antiSMASH that each contain only one BGC. These files will be searched in all locations of designated input directory. All other files (e.g. Genbank file that contains more than one BGC) will be ignored (but not removed from its directory).
> The metadata of Genbank files of selected BGCs, e.g. the location of the Genbank files in the input directory, will not be provided.
> If no BGC should be selected by second-chance selection, the parameter for this selection round (i.e. "minimum number of additional genes") can be set to a high number, e.g. 1000.
> If all BGCs should be selected for the next task (e.g. because all BGCs are already complete BGCs detected from complete genomes and therefore no BGC-selection is needed, rather user only needs to know e.g. the product statistics of the detected BGCs from task 1), all selection parameters can be set to 0. Alternatively, put all Genbank files containing the input BGCs, if these are available, in the directory "input_for_BiGSCAPE" and skip to task 3.
> The results of this task (i.e. Genbank files of detected and selected BGCs, statistics of BGC-selection and product(s) of detected and selected BGCs) can be found in the directory "selected_BGCs" and "statistics".

>> Task 3 (clustering of similar BGCs by BiG-SCAPE CORASON):
> This pipeline searches and analyzes in this task Genbank (.gbk) files generated by antiSMASH that each contain only one BGC. These files will be searched in all locations of designated input directory. All other files (e.g. Genbank file that contains more than one BGC) will be ignored (but not removed from its directory).
> The results of this task (i.e. similarity analysis) can be viewed in HTML-format by clicking on the "index.html" file, which is located in the designated output directory.

>> General tips:
> In case many input files have duplicate name but different content, the option "analyze_files_with_same_name_but_different_content" in module "side_options.py" should be set to True.
> Alternatively, the input files can be separated into many input directories, then each directory analyzed with the pipeline separately. For task 3 (similarity analysis), this however will yield different results as the BGCs will not be analyzed together.
> In case there are input files that have same name and also contain data for the same BGC, the option "analyze_files_with_same_name_but_different_content" in module "side_options.py" should be set to False. This will avoid analyzing same files multiple times.
> In case there are input files that have different names but contain data for the same BGC, these files can all be analyzed and later identified as duplicate BGCs on the similarity network created by BiG-SCAPE CORASON.

________________________________________________________________________________________________________________________
