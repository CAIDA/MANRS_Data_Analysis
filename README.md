# MANRS_Data_Analysis

This repo contains analysis code used in the paper [Mind Your MANRS: Measuring the MANRS Ecosystem](https://www.caida.org/catalog/papers/2022_mind_your_manrs/mind_your_manrs.pdf) from IMC 2022. The analysis code provides certain details that were obscured in the paper.

[MANRS - Mutually Agreed Norms on Routing Security](https://www.manrs.org/)
- [MANRS Actions for Network Operators](https://www.manrs.org/netops/network-operator-actions/)
- [MANRS Actions for CDNs and Cloud Providers](https://www.manrs.org/cdn-cloud-providers/actions/)

The Jupyter notebooks can be used to check the conformance of MANRS networks if you provide the most recent data files.

## Installation
Jupyter notebook is required to run the notebooks. In addition, the notebooks are organized using the `Table of Contents(2)` feature in package `nbextensions`. The installation guide for nbextensions is in its [documentation](https://jupyter-contrib-nbextensions.readthedocs.io/en/latest/install.html).

## Running the notebooks
The revelant notebooks to the paper are:  
- [MANRS_Conformance_Action1](https://github.com/CAIDA/MANRS_Data_Analysis/blob/master/MANRS_Conformance_Action1.ipynb)
- [MANRS_Conformance_Action4](https://github.com/CAIDA/MANRS_Data_Analysis/blob/master/MANRS_Conformance_Action4.ipynb)

The notebooks are runnable as-is in the repository directory with provided data files. A list of MANRS networks that are **not conformant** to the corresponding actions will appear at the end of the notebooks. If you are using the `Table of Contents(2)` extensions, the revelant sections are highlighted.

To look at the most recent conformance levels of MANRS networks, you can run the notebooks on more recent data. There are cell blocks with input file paths that can be replaced. They are marked with `#replace with new file`.
