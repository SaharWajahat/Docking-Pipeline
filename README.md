# Docking-Pipeline

A clean, reproducible AutoDock Vina docking workflow for structure-based drug discovery. 

**Features**
- **Receptor prep**: Clean PDB, add hydrogens, remove waters
- **Ligand prep**: 2D to 3D with Open Babel  
- **Docking**: AutoDock Vina with grid setup
- **Analysis**: Auto CSV + Top5 bar plot + Score distribution histogram

**Run on Google Colab**
```bash
!git clone https://github.com/SaharWajahat/Docking-Pipeline.git
%cd Docking-Pipeline
!pip install openbabel matplotlib pandas
!python docking_pipeline.py --receptor protein.pdb --ligand ligand.smi
```

**Outputs**
- `results/docking_scores.csv` : All binding affinities
- `results/top5_bar.png` : Top 5 ligands by affinity
- `results/score_distribution.png` : Histogram of all scores with -7.0 cutoff

**Status**: MD simulation and free energy workflow in progress. 
Built for GPCR drug discovery research.

**License**: MIT 

**Author**: Sahar Wajahat, 2026
