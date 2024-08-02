# Sap2000py

Sap2000py is a python module to interact with Sap2000 API

This Demo below shows how to interact with SAP2000 using the Sap2000py library. The project includes complete examples of creating and manipulating SAP2000 models, running analyses, and exporting results to Excel.

## Contents

- [Installation](#installation)
- [Usage](#usage)
  - [Setting the Model Path](#setting-the-model-path)
  - [Creating and Opening a SAP2000 Project](#creating-and-opening-a-sap2000-project)
  - [Model Information](#model-information)
  - [Adding Materials and Elements](#adding-materials-and-elements)
  - [Analysis](#analysis)
  - [Post-processing](#post-processing)
  - [Saving and Closing](#saving-and-closing)
- [Dependencies](#dependencies)

## Installation

1. Clone this repository to your local machine.
2. Install the dependencies:

```bash
pip install Sap2000py
```

## Usage

Below are detailed instructions for using `Sap2000pyDemo.py`.

### Setting the Model Path

At the beginning of the script, set the path to your model file:

```python
ModelPath = 'F:\\python\\Sap2000\\Models\\Test.sdb'
```

### Creating and Opening a SAP2000 Project

Create a Sap2000py object and open the SAP2000 program:

```python
from Sap2000py.Saproject import Saproject

Sap = Saproject()
Sap.openSap()
Sap.File.Open(ModelPath)
```

### Model Information

Get basic information about your SAP2000 project:

```python
Sap.getSapVersion()
Sap.getProjectInfo()
Sap.getUnits()
```

Make changes to the model:
```python
# Set the project information with field and value
Sap.setProjectInfo("Author","Gou Lingyun")
Sap.setProjectInfo("Description","This is a test model")

# or you can set project information with a dictionary
Sap.setProjectInfo(info_dict={"Author":"Gou Lingyun","Description":"This is a test model"})

# Set the units of the model
Sap.setUnits("KN_m_C")
```

### Adding Materials and Elements

Add materials and elements to the model:

```python
# Add China Common Material Set·
Sap.Scripts.AddCommonMaterialSet(standard = "JTG")

# Add Joints and Elements
joint_coord = np.array([[0,0,0], [10,0,0], [20,0,0], [30,0,0]])
Sap.Scripts.AddJoints(joint_coord)
Sap.Scripts.AddElements([[1,2], [2,3], [3,4]])
```

### Analysis

Run a modal analysis:

```python
Sap.Scripts.Analyze.RemoveCases("All")
Sap.Scripts.Analyze.AddCases(Casename = ['DEAD', 'MODAL'])
Sap.Scripts.Analyze.RunAll()
```

### Post-processing

Export analysis results to an Excel file:

```python
filename = 'F:\\python\\Sap2000\\Models\\Test.xlsx'
wb = openpyxl.load_workbook(filename)
ws = wb.worksheets[0]

Sap.Scripts.SelectCombo_Case(["DEAD"])
Name, EleAbsForce, __, __ = Sap.Scripts.GetResults.ElementJointForce_by_Group("PierBottom")
Sap.Scripts.writecell(ws, EleAbsForce[:,[2]], "D22")

wb.save(filename)
```

### Saving and Closing

Save the project and close the SAP2000 program:

```python
Sap.File.Save()
Sap.closeSap()
```

## Dependencies

- python>=3.9

This project requires the following Python libraries:

- numpy
- os
- openpyxl
- comtypes>=1.1.11
- itertools
- rich
- loguru
- pathlib
- json
- sectionproperties>=3.3.0

For more information, please check [Sap2000pyDemo.py](./Sap2000pyDemo.py).
