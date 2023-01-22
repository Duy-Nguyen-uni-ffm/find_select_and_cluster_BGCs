INSTRUCTIONS FOR SETUP AND RUNNING THE BIOINFORMATIC PIPELINE

>>> Short description of the bioinformatic pipeline:

> FUNCTION: This pipeline is developed to (1) find biosynthetic gene clusters (BGCs) on all DNA sequences given in FASTA file(s), (2) select from all identified BGCs the ones that can be considered as complete and functional BGCs, and (3) analyze the similarity between the selected BGCs and the well-known BGCs from the database MIBiG.
> INPUT:    One or many FASTA files. These files need to be located inside the designated input directory (which is specifically "input_for_antiSMASH").
> OUTPUT:   Output of all three mentioned tasks can be found in the designated directories (which are specifically "output_from_antiSMASH", "selected_BGCs", "statistics" and "output_from_BiGSCAPE").

________________________________________________________________________________________________________________________


SYSTEM REQUIREMENTS (IMPORTANT)

> This pipeline should be operated on a Linux system (other systems e.g. Windows not tested). If not available on local computer, a virtual Linux system can be downloaded from e.g. the provider Oracle VM VirtualBox and set up on local computer (links for downloading all required components and instructions for setting up the virtual system can be found on e.g. https://www.youtube.com/watch?v=wX75Z-4MEoM (ca. 30 minutes). Download and setup of the virtual system take about 60 minutes. Host system, e.g. Windows, will not be affected). Furthermore, a Python version > 3.9 should be available on the Linux system.
> This pipeline requires approx. 17 Gb on hard disk for setup and at least 2 CPUs and 2 Gb on RAM for an efficient operation.

________________________________________________________________________________________________________________________


SETUP (IMPORTANT)

>>> Command for installing two utility tools (curl and docker, if not available on system), and the two required third-party programs (latest versions of both), which are antiSMASH and BiG-SCAPE CORASON, to the designated directory "thirdparty_programs" (if the two programs not preinstalled on local computer or installed in different locations):

> Run all-in-one setup file "setup.py" by typing in Terminal (opened in common directory, that is, directory that contains all files of pipeline):
python setup.py
> Note: a different python command to run this setup file can be used, e.g. python3 setup.py. First time setup will take about 5 minutes. An internet connection is needed for this setup. During setup, certain input from user will be needed e.g. user password, confirmation to download certain packages.
> Enable permission to execute pipeline:
chmod +x run_pipeline

________________________________________________________________________________________________________________________


RUN (IMPORTANT)

>>> Command for running pipeline (only after running setup or if required programs already preinstalled in designated folder):

> Create a folder with the specific name "input_for_antiSMASH" in the common directory (i.e. directory containing all scripts of pipeline) and move FASTA input file(s) containing DNA sequence(s) to be analyzed in the folder. No specific location for the input file(s) inside the folder is required, i.e. the input file(s) can be placed anywhere inside the input directory (still, they can all be found by the pipeline).
> Run the pipeline by typing in Terminal (also in common directory):
./run_pipeline
> Note: user password might be needed at the beginning of every run as pipeline is executed with sudo, i.e. root privileges!
> Note: at the very first run of pipeline with task 1 and/or 3, certain large-sized packages will be installed for antiSMASH and BiG-SCAPE CORASON. This installation only happens at the very first run of pipeline, and will take about 40 minutes. In the next runs, no further installation will be executed.

________________________________________________________________________________________________________________________


>>> Further information to setting up and running this pipeline:

> For manual installation of antiSMASH: https://docs.antismash.secondarymetabolites.org/install/
> For manual installation of BiG-SCAPE CORASON: https://bigscape-corason.secondarymetabolites.org/installation/index.html
> In order to execute task 1 (finding BGCs by antiSMASH) and task 3 (clustering of similar BGCs by BiG-SCAPE CORASON) with this pipeline, installation of the programs antiSMASH and BiG-SCAPE CORASON to the directory "thirdparty_programs" specifically is required. These programs can be acquired with the setup file "setup.py" and installation steps described above.
> In task 2 of this pipeline (i.e. BGC-selection), Genbank files created by antiSMASH (e.g. in task 1) should be input for this task. External Genbank files created by other software or for other purposes might not be compatible for task 2 of pipeline.
> A scheme for the workflow of this pipeline as well as a scheme of the BGC-selection algorithm used in task 2 can be found in the directory "info".
> This pipeline can only detect and analyze biosynthetic gene clusters (BGCs) encoding polyketides, peptides, terpenes, etc. that can be found on bacterial genomes (for finding BGCs on fungal or plant genomes, the option "--genefinding-tool" in file "run_antismash.py" must be adjusted).
> An internet connection is recommended for running pipeline, although not necessarily needed for the execution of task 1, 2 and 3 of the pipeline, to allow the pipeline to access to the latest databases.

________________________________________________________________________________________________________________________


>>> Notes/tips:

>> General notes:
> Each of the executable task in this pipeline can be executed independently (i.e. this pipeline does not have to necessarily start with task 1 by every run), provided that the required input data (as zipped files/folders or unzipped files) are given in the corresponding input directory for the task.
> If a Python library needed for the execution of the pipeline is not yet installed on local computer (e.g. pandas, tabulate), this can be installed by typing the command: pip install <NAME OF LIBRARY>
> The module "side_options.py" contains all options that can be adjusted for a customized usage of the pipeline, e.g. option to use predefined values for parameters so there is no need to input values for these parameters by every run.
> Output directories of all tasks can be emptied before executing task by adjusting the corresponding options in module "side_options.py". All files and folders in input directory for task 1 (gene prediction by antiSMASH) however will never be removed.

>> Task 1 (gene finding by antiSMASH):
> This pipeline can only analyze as input for this task FASTA files. One or many FASTA input files must be in the designated directory "input_for_antiSMASH". These files will be searched in all locations inside the designated input directory.
> This task takes on average approx. 5 minutes for one complete bacterial genome.
> The results of this task (i.e. detection of BGCs) can be viewed in HTML-format by clicking on the "index.html" file, which is located in the output directory "output_from_antiSMASH".

>> Task 2 (BGC-selection):
> This pipeline searches and analyzes in this task Genbank (.gbk) files, which should be ideally generated by antiSMASH, that each contain only one BGC. These files will be searched in all locations inside the designated input directory for the task, i.e. "output_from_antiSMASH". All other files (e.g. Genbank file that contains more than one BGC) will be ignored (but not removed from the directory).
> The metadata of Genbank files of selected BGCs, e.g. the location of the Genbank files in the input directory, will not be provided.
> If no BGC should be selected by second-chance selection, the parameter for this selection round (i.e. "minimum number of additional genes") can be set to a high number, e.g. 1000.
> If all BGCs should be selected for the next task (e.g. because all BGCs are already complete BGCs detected from complete genomes and therefore no BGC-selection is needed, rather user only needs to know e.g. the product statistics of the detected BGCs from task 1), all selection parameters can be set to 0. Alternatively, one can also put all the Genbank files directly in the directory "input_for_BiGSCAPE" (this directory must be created manually) and skip to task 3.
> This task takes on average approx. 5 minutes for all BGCs detected on a complete bacterial genome.
> The results of this task (i.e. Genbank files of selected BGCs, statistics of BGC-selection and product(s) of selected BGCs) can be found in the directory "selected_BGCs" and "statistics".

>> Task 3 (clustering of similar BGCs by BiG-SCAPE CORASON):
> This pipeline searches and analyzes in this task Genbank (.gbk) files, ideally generated by antiSMASH, that each contain only one BGC. These files will be searched in all locations inside the directory "selected_BGCs". All other files (e.g. Genbank file that contains more than one BGC) will be ignored (but not removed from the directory).
> This task takes on average approx. 60 minutes for all BGCs of one complete bacterial genome.
> The results of this task (i.e. similarity analysis of the BGCs) can be viewed in HTML-format by clicking on the "index.html" file, which is located in the designated output directory "output_from_BiGSCAPE".

>> General tips:
> In case many input files have duplicate name but different content, the option "analyze_files_with_same_name_but_different_content" in module "side_options.py" should be set to True.
> Alternatively, the input files can be separated into many input directories, then each directory analyzed with the pipeline separately. For task 3 (similarity analysis), this however will yield different results as the BGCs will not be analyzed together.
> In case there are input files that have same name and also contain data for the same BGC, the option "analyze_files_with_same_name_but_different_content" in module "side_options.py" can be set to False. This will avoid analyzing same files multiple times.
> In case there are input files that have different names but contain data for the same BGC, these files can all be analyzed and later identified as duplicate BGCs on the similarity network created by BiG-SCAPE CORASON.

________________________________________________________________________________________________________________________
