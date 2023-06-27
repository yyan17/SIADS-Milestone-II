SL FOLDER ReadMe
This text was Last updated on: 20230626

Notebooks:
1. SL_base_dataset_2023_06.ipynb:
	- Inputs: all 22 raw files from group 15 github page (https://github.com/yyan17/SIADS-Milestone-II/tree/add_new_datasets/datasets/raw/supervised_learning)
	- Output: sl_base_dataset_2023_06.csv
	

2. SL_Derived_Dataset_2023_06.ipynb (**updated version)
	- Input: sl_base_dataset_2023_06.csv
	- Output:  sl_derived_dataset_2023_06.csv
		Update: two new points-won columns (FTHP, FTAP)


3. pycaret_2023_06_22.ipynb (**updated version)
	- input: sl_base_dataset_2023_06.csv; sl_derived_dataset_2023_06.csv
	- output: 
        - SL normalized model results: base dataset only/ derived dataset only; 
        - Four pycaret runs using a mix of features from the two input files.
