"# Thermal-Data-Analysis" 
1. Install conda for managing virtual environments- [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/linux.html)
 ```
   conda env create -f environment.yml
 
   conda activate venv
   ```
2. ```
   python main.py 
   ``
  the script expect a yaml file containing the bounding boxes of the region of interest. the temp data around this bounding box is computed and analysis is performed to determine how this temp data in the region of interest varies for **N** number of images
