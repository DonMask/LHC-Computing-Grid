# LHC Computing Grid Optimization for High-Luminosity LHC

This repository contains the source code, documentation, and supplementary materials for the paper "Optimizing Task Allocation in the LHC Computing Grid for the High-Luminosity LHC Using a Heuristic Approach" by Teodor Berger. The project develops a mathematical model and a hybrid heuristic algorithm (greedy + simulated annealing) to optimize task allocation in the LHC Computing Grid, achieving a 36% reduction in energy consumption and a 3.6% reduction in processing time for HL-LHC data processing.

## Project Overview
The High-Luminosity Large Hadron Collider (HL-LHC), set to operate from 2028, will generate 1.4 PB of data daily. This project addresses the computational challenges by optimizing task allocation across 170 heterogeneous nodes in the LHC Computing Grid. Key features:
- **Mathematical Model**: Multi-objective linear programming to minimize processing time and energy consumption.
- **Heuristic Algorithm**: Greedy initialization with simulated annealing for scalability ($N=170$, $M=5000$).
- **Results**: 384 GWh annual energy savings for 100 clusters, 76.85 million € cost reduction, and 3.6% faster processing.
- **Validation**: Exceeds CERN’s 17.4% energy efficiency target.

The paper is published on Zenodo with DOI: [10.5281/zenodo.15477551](https://doi.org/10.5281/zenodo.15477551).

## Repository Structure
- `LICENSE`: Creative Commons Attribution 4.0 International (CC BY 4.0) license.
- `README.md`: Project overview and instructions.
- `main.pdf`: Compiled paper.
- `main.tex`: LaTeX source for the paper.
- `optimization_chart.png`: Bar chart of optimization results.
- `generate_chart.py`: Python script to generate `optimization_chart.png`.

## Installation and Usage
### Prerequisites
- Python 3.x with `matplotlib` and `numpy` for chart generation.
- LaTeX distribution (e.g., TeX Live) for compiling `main.tex`.
- Overleaf (optional) for editing and compiling LaTeX.

### Generate Optimization Chart
Run the Python script to generate the chart used in the paper:
```bash
pip install matplotlib numpy
python generate_chart.py
```
This creates optimization_chart.png in the repository root.
Compile LaTeX
To compile main.tex locally:
```bash
pdflatex main.tex
```
Or upload to Overleaf and compile with default settings.

## License
This project is licensed under the Creative Commons Attribution 4.0 International (CC BY 4.0) license. You are free to:
•  Share: Copy and redistribute the material in any medium or format.
•  Adapt: Remix, transform, and build upon the material for any purpose, even commercially.
Under the following terms:
•  Attribution: You must give appropriate credit to the author (Teodor Berger), provide a link to the license, and indicate if changes were made.
•  No additional restrictions: You may not apply legal terms or technological measures that restrict others from doing anything the license permits.
See the LICENSE file for the full license text.
Acknowledgments
This work is inspired by CERN’s efforts to enhance computational efficiency for the HL-LHC. Special thanks to the open-source community for tools like LaTeX, Python, and Matplotlib.

# Citation
Please cite this work as:
```bash
Berger, T. (2025). Optimizing Task Allocation in the LHC Computing Grid for the High-Luminosity LHC Using a Heuristic Approach. Zenodo. https://doi.org/10.5281/zenodo.15477551
```
Author
___
•  Name: Teodor Berger
•  Email: bergerteodor@googlemail.com
