# ARBoLoM (**A**SP-based **R**evision of **B**oolean **L**ogical **M**odels)
The ARBoLoM tool aims to automate the revision of Boolean logical models, with fully Answer Set Programming-based consistency checking and repair algorithms. 

## Encoding Directories
The encodings responsible for verifying the consistency of a model given [stable state](https://github.com/fpaleixo/arbolom/blob/main/encodings/consistency/ss_consistency.lp), [synchronous](https://github.com/fpaleixo/arbolom/blob/main/encodings/consistency/sync_consistency.lp), or [asynchronous observations](https://github.com/fpaleixo/arbolom/blob/main/encodings/consistency/async_consistency.lp), can be found [here](https://github.com/fpaleixo/arbolom/tree/main/encodings/consistency).

The encodings responsible for repairing a function using [stable state](https://github.com/fpaleixo/arbolom/blob/main/encodings/repairs/repairs_stable.lp), [synchronous](https://github.com/fpaleixo/arbolom/blob/main/encodings/repairs/repairs_sync.lp), or [asynchronous observations](https://github.com/fpaleixo/arbolom/blob/main/encodings/repairs/repairs_async.lp), can be found [here](https://github.com/fpaleixo/arbolom/tree/main/encodings/repairs).

## Installation (2 alternatives)

### Using Google Colab
All scripts can be tested with no installation by using Google Colab. Just download the repository and change the working directory to the arbolom folder.

### Using a local installation
For a local installation, Python 3.6 or above is required, alongside the [clingo package](https://pypi.org/project/clingo/). Detailed instructions can be found in the [potassco website](https://potassco.org/clingo/).

## Running the Scripts

Instructions and examples on how to run each script can be found in the [notebook](https://github.com/fpaleixo/arbolom/blob/main/ARBoLoM.ipynb) file.

## Quick Testing
For quick testing, the models in the [simple_models](https://github.com/fpaleixo/arbolom/blob/main/simple_models) folder may be used. These are small, hand-made examples of hypothethical biological networks. Due to their compact nature, one can use them to perform quick tests with the scripts, or to manually verify the correctness of the results produced by said scripts.

Generally, the models will be used in the following fashion:
- One of the models is chosen to perform tests on. 
- The `corruption.py` script can then be used to create a "wrong" version of this model.
- `conversion.py` is ran on both models, to convert them to .lp format.
- `gen_observations.py` is ran on the original .lp model, to generate observations that can be used to check the correctness of the wrong model.
- `revision.py` is ran on the corrupted model alongisde the generated observations, to revise it. 

Note: Alternatively, instead of using `revision.py`, `consistency_checking.py` can also be used on the inconsistent .lp model, alongside the observations generated from the original model. This script will tell you if the model is consistent with the given observations or not. In case it is not, the inconsistencies generated can then be given to `repair.py`, which will repair the inconsistent model (`revision.py` simply streamlines this process, doing it all at once).


## Task Progress

[![Task 1 - Create simple models](https://img.shields.io/badge/Task_1-Create_simple_models-green?style=for-the-badge&logo=Adobe+Acrobat+Reader)](https://github.com/fpaleixo/arbolom/tree/main/simple_models) 
[![Task 2 - Script for model corruption](https://img.shields.io/badge/Task_2-Script_for_model_corruption-green?style=for-the-badge&logo=python)](https://github.com/fpaleixo/arbolom/blob/main/corruption.py)
[![Task 3 - Script for model conversion](https://img.shields.io/badge/Task_3-Script_for_model_conversion-green?style=for-the-badge&logo=python)](https://github.com/fpaleixo/arbolom/blob/main/conversion.py)
[![Task 4 - Encodings to create observations](https://img.shields.io/badge/Task_4-Encodings_to_create_observations-green?style=for-the-badge&logo=dev.to)](https://github.com/fpaleixo/arbolom/tree/main/encodings)
[![Task 5 - Encodings for model consistency](https://img.shields.io/badge/Task_5-Encodings_for_model_consistency-green?style=for-the-badge&logo=dev.to)](https://github.com/fpaleixo/arbolom/tree/main/encodings)
![Task 6 - Define repair strategy](https://img.shields.io/badge/Task_6-Define_repair_strategy-green?style=for-the-badge&logo=Adobe+Acrobat+Reader)
[![Task 7 - Encodings to repair models](https://img.shields.io/badge/Task_7-Encodings_to_repair_models_(and_respective_optimizations)-green?style=for-the-badge&logo=dev.to)](https://github.com/fpaleixo/arbolom/tree/main/encodings)
![Task 8 - Benchmarking and writing the document](https://img.shields.io/badge/Task_8-Benchmarking_and_writing_the_document-yellow?style=for-the-badge&logo=dev.to)

### Timestamps (relative*)

Task 1: Week 1 (07/03 to 09/03)

Task 2: Week 1-2 (09/03 to 17/03)

Task 3: Week 2-3 (17/03 to 21/03)

Task 4: Week 3-4 (21/03 to 28/03)

Task 5: Week 4-5 (28/03 to 05/04)

Task 6: Week 5-6 (05/04 to 11/04)

Task 7: Week 6-21 (11/04 to 01/08)

Task 8: Week 20-*ongoing* (29/07 to 30/09)

\* *for reference only - dates are not absolutely exact and deliverables usually suffer tweaks/changes after these  periods*



##

This work is licensed under a
[Creative Commons Attribution 4.0 International License][cc-by].

[![CC BY 4.0][cc-by-image]][cc-by]

[cc-by]: http://creativecommons.org/licenses/by/4.0/
[cc-by-image]: https://i.creativecommons.org/l/by/4.0/88x31.png
[cc-by-shield]: https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg
