# ARGOS_fair_qi

# FAIR_QI

FAIR Quantitative Imaging toolbox


## Build Status

| Linux                          | Mac OS                        | Windows                       |
|--------------------------------|-------------------------------|-------------------------------|
| Passed                         | Not Available                 | Passed                        |

# FAIR-QI
## Findable(F), Accessible(A), Interoperability(I) and Reuse(R) - Quantitative(Q) Imaing(I)

Welcome to FAIR-Quantitative Imaging (FAIR-QI) repository.
FAIR-QI provides a suggested analysis workflow for quantitative imaging including not only conventional radiomics or deep learning-based radiomics, but also deep neural networks. The process starts from DICOM file that is the most commonly used medical image format in clinical practice and ends with multiple quantitative imaging features.

Note that, the source code of the current repository only shows part of the functions of FAIR-QI package, that is, generattion of DICOM Segmentation from DICOM files. More source codes will be uploaded soon.

## Citation
Please cite the reposiotry when you use it for academic research.

## *** Warning

The current version of FAIR-QI is developed on Ubuntu 16.04. The program works on Ubuntu 16.04 or higher, Windows 10. Due to plastimatch installation, the verison of FAIR-QI for Mac OS is not available now.

## Disclaimer

FAIR-QI is still under development. Although we have tested and evaluated the workflow under many different situations, errors and bugs still happen unfortunately. Please use it cautiously. If you find any, please contact us and we would fix them ASAP.


### Prerequisites 

FAIR-QI dependents on several main tools and packages that are listed below.

* [Anaconda3](https://www.anaconda.com/download) python version 3, which includes python and hundreds of popular data science packages and the conda package and virtual environment manager for Windows, Linux, and MacOS. Note that, Python = 3.7.
* [dcmqi](https://github.com/QIICR/dcmqi) - Convert certain types of quantitative image analysis results into standardized DICOM form.
* [plastimatch](https://www.plastimatch.org/) - For windows/Linux user, convert RTSTRUCT to binary mask.


### Installation

Implement the following code, first go to directory /ARGOS/
* Windows: add dcmqi/bin PATH to enviroment variable
* Linux: 
```
export PATH="$(pwd)/dcmqi_linux/bin":$PATH" 
```
* Installation of dependent packages

Execute:

```
cd /Script
python -m pip install -r QI_requirements.txt
```

### Getting Started

Converting DCM to SEG object, execute:
```
python QI_DCMRT2SEG_main.py
```
Converting SEG object to ITK image, execute:
```
python QI_SEG2ITKimage.py
```
The NRRD ITK images are stored in 
```
/ARGOS/output/ITKimage_CT/
```
The NRRD ITK mask are stored in 
```
/ARGOS/output/ITKimage_mask/
```
Specifically for GTV NRRD mask generation, implement the following script. 

```
python QI_extract_gtv_nrrd.py
```
Then all GTV-related ROIs of each patient will be stored in folders under the /output/ directory.

### For your study

* Remove the example data in 
```
/ARGOS/Data/
```
* Copy your data to the directory above.
* Then follow the processing steps above.

## License

FAIR-QI may not be used for commercial purposes. This package is freely available to browse, download, and use for scientific and educational purposes as outlined in the [Creative Commons Attribution 3.0 Unported License](https://creativecommons.org/licenses/by/3.0/).

## Developers
 - [Zhenwei Shi](https://github.com/zhenweishi)<sup>1</sup>
 - [TianChen Luo] 
 - [Leonard Wee]<sup>1</sup>
 - [Andre Dekker]<sup>1</sup>
 
<sup>1</sup>Department of Radiation Oncology (MAASTRO Clinic), GROW-School for Oncology and Development Biology, Maastricht University Medical Centre, The Netherlands.


### Contact
We are happy to help you with any questions. Please contact Zhenwei Shi.
Email: zhenweishi88@163.com

We welcome contributions to FAIR-QI.