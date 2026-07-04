# Docking-Pipeline

A clean, reproducible AutoDock Vina docking workflow for structure-based drug discovery. 

**Features**
- **Receptor prep**: Clean PDB, add hydrogens, remove waters
- **Ligand prep**: 2D to 3D with Open Babel  
- **Docking**: AutoDock Vina with grid setup
- **Analysis**: Auto CSV + Top5 bar plot + Score distribution histogram
- **Auto-download**: Results are saved and downloaded at each step to prevent data loss

**Run on Google Colab**

[[Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/SaharWajahat/Docking-Pipeline/blob/main/Vina_Docking_Workflow.ipynb)

**How to run:**
1. Click the "Open in Colab" badge above
2. Run cells **one by one** from top to bottom
3. When prompted, upload your `receptor.pdb` file
4. When prompted, upload your `ligand.smi` file  
5. Continue running each cell to complete docking and analysis
6. Files auto-download after each major step. Check your `Downloads` folder

**Outputs**
- `results/docking_scores.csv` : All binding affinities
- `results/top5_bar.png` : Top 5 ligands by affinity
- `results/score_distribution.png` : Histogram of all scores with -7.0 cutoff

**Status**: MD simulation and free energy workflow in progress. 
Built for drug discovery research.

**License**: MIT 

**Author**: Sahar Wajahat, 2026
