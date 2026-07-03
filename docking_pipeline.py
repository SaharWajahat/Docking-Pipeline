"""
===============================================================================
Docking-Pipeline v1.0.0
Author: Sahar Wajahat 
Date: 2026-09-04
Purpose: Reproducible AutoDock Vina workflow for drug discovery 
===============================================================================
"""

import os
import subprocess
import pandas as pd
import matplotlib.pyplot as plt

# ==============================================================================
# SECTION 1: RECEPTOR PREPARATION 
# Colab Logic: Clean PDB HETATM|WAT + OpenBabel to PDBQT
# ==============================================================================
def prepare_receptor(input_pdb="receptor.pdb"):
    """
    Cleans PDB and converts to PDBQT format for Vina.
    NOTE: !obabel removed for GitHub. Creates dummy file for demo.
    """
    print(f"[1/5] SECTION 1: RECEPTOR PREPARATION")
    
    protein_clean = "protein_clean.pdb"
    if not os.path.exists(protein_clean):
        with open(protein_clean, "w") as f:
            f.write("ATOM      1  N   ALA A   1       0.000   0.000   0.000 1.00 0.00\n")
        print(f"      -> Created: {protein_clean}")
    
    output_pdbqt = "receptor.pdbqt"
    if not os.path.exists(output_pdbqt):
        with open(output_pdbqt, "w") as f:
            f.write("REMARK Dummy PDBQT for GitHub demo\n")
        print(f"      -> Created: {output_pdbqt}\n")
    else:
        print(f"      -> Found: {output_pdbqt}\n")
        
    return output_pdbqt


# ==============================================================================
# SECTION 2: LIGAND PREPARATION
# Colab Logic: SMILES .smi file -> OpenBabel -> ligands_pdbqt/ folder
# ==============================================================================
def prepare_ligands(smiles_file="top50.smi", num_ligands=50):
    """
    Converts SMILES to PDBQT ligands using OpenBabel.
    NOTE: !obabel removed for GitHub. Creates dummy files for demo.
    """
    print(f"[2/5] SECTION 2: LIGAND PREPARATION")

    ligands_dir = "ligands_pdbqt"
    os.makedirs(ligands_dir, exist_ok=True)

    if not os.path.exists(smiles_file):
        with open(smiles_file, "w") as f:
            for i in range(1, num_ligands + 1):
                f.write(f"CCO\tLIG_{i:03d}\n")
        print(f"      -> Created dummy: {smiles_file}")

    for i in range(1, num_ligands + 1):
        lig_file = os.path.join(ligands_dir, f"lig_{i:03d}.pdbqt")
        if not os.path.exists(lig_file):
            with open(lig_file, "w") as f:
                f.write(f"REMARK Dummy ligand {i}\n")
    
    num_files = len([f for f in os.listdir(ligands_dir) if f.endswith('.pdbqt')])
    print(f"      -> Actual count: {num_files} ligands converted ✓\n")
    return ligands_dir


# ==============================================================================
# SECTION 3: DOCKING WITH VINA
# Colab Logic: Loop 1-50, subprocess.run vina, parse affinity, save CSV
# Box: --center_x 40 --center_y 40 --center_z 40 --size_x 20 ...
# ==============================================================================
def run_docking(receptor_pdbqt, ligands_dir, num_ligands=50):
    """
    Runs AutoDock Vina for all ligands. 
    NOTE: Real vina call removed for GitHub. Creates dummy scores for demo.
    """
    print(f"[3/5] SECTION 3: DOCKING WITH VINA")
    
    box = "--center_x 40 --center_y 40 --center_z 40 --size_x 20 --size_y 20 --size_z 20"
    print(f"      -> Box params: {box}")
    
    os.makedirs("results", exist_ok=True)
    csv_path = "results/docking_scores.csv"
    
    results = []
    for lig_id in range(1, num_ligands + 1):
        pdbqt_path = os.path.join(ligands_dir, f"lig_{lig_id:03d}.pdbqt")
        
        if not os.path.exists(pdbqt_path):
            aff = "NA"
        else:
            # DEMO MODE: Dummy affinity instead of real vina call
            aff = round(-9.5 + (lig_id * 0.04), 1) # Dummy data from -9.5 to -7.5
        
        results.append({"Ligand": f"LIG_{lig_id:03d}", "Affinity_kcal/mol": aff})
        print(f"      -> Ligand {lig_id:03d}: {aff} kcal/mol")

    df = pd.DataFrame(results)
    df.to_csv(csv_path, index=False)
    print(f"      -> Saved: {csv_path}\n")
    return df

# ==============================================================================
# SECTION 4: POST-PROCESSING - TOP5 EXPORT [YOUR NEW CODE]
# ==============================================================================
def export_top5(df):
    """
    Your Colab code: Reads df, gets Top5, prints, saves to CSV.
    Runs BEFORE plotting.
    """
    print(f"[4/5] SECTION 4: EXPORT TOP5")
    df_numeric = df[df['Affinity_kcal/mol'] != 'NA'].copy()
    df_numeric['Affinity_kcal/mol'] = df_numeric['Affinity_kcal/mol'].astype(float)
    
    # YOUR CODE FROM PHOTO - ADDED HERE
    df = pd.read_csv("results/docking_scores.csv")
    top5 = df_numeric.sort_values("Affinity_kcal/mol").head(5)
    print(top5.to_string(index=False)) # Print table
    top5.to_csv("results/top5_ligands.csv", index=False) # Save CSV
    print(f"      -> Saved: results/top5_ligands.csv ✅\n")
    
    return top5 # Return for plotting

# ==============================================================================
# SECTION 5: PLOTTING RESULTS 
# Bar: top5 only | Hist: df = all smiles
# ==============================================================================
def plot_results(df):
    """
    Creates Top5 bar plot and Score distribution histogram for ALL ligands.
    Styling : figsize=(8,5), dpi=300, teal, coral, bold.
    """
    print(f"[5/5] SECTION 4: PLOTTING")
    df_numeric = df[df['Affinity_kcal/mol'] != 'NA'].copy()
    df_numeric['Affinity_kcal/mol'] = df_numeric['Affinity_kcal/mol'].astype(float)
    
    top5 = df_numeric.sort_values("Affinity_kcal/mol").head(5)

    # 1. Bar Chart - TOP 5 ONLY
    plt.figure(figsize=(8, 5))
    plt.bar(top5['Ligand'].astype(str), top5['Affinity_kcal/mol'], color='teal')
    plt.title("Top 5 Ligands by Binding Affinity", fontsize=14, weight='bold')
    plt.xlabel("Ligand ID", fontsize=12)
    plt.ylabel("Affinity (kcal/mol)", fontsize=12)
    plt.gca().invert_yaxis() # Lower is better for docking
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.savefig("results/top5_bar.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("      -> Saved: results/top5_bar.png")

    # 2. Histogram - ALL 50 SMILES, NOT TOP5
    plt.figure(figsize=(8, 5))
    plt.hist(df_numeric['Affinity_kcal/mol'], bins=15, color='coral', edgecolor='black') # df_numeric = all 50
    plt.title("Distribution of Docking Scores", fontsize=14, weight='bold')
    plt.xlabel("Affinity (kcal/mol)", fontsize=12)
    plt.ylabel("Number of Ligands", fontsize=12)
    plt.axvline(x=-7.0, color='red', linestyle='--', linewidth=2, label='Hit Cutoff <-7.0')
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.savefig("results/score_distribution.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("      -> Saved: results/score_distribution.png\n")
    
    print("Plots saved to results/ folder ✅")


# ==============================================================================
# MAIN ENTRY POINT
# ==============================================================================
def main():
    print("\n================ Docking-Pipeline Starting ================\n")
    
    receptor_file = prepare_receptor()
    ligands_dir = prepare_ligands(num_ligands=50)
    df_scores = run_docking(receptor_file, ligands_dir, num_ligands=50)
    plot_results(df_scores)
    
    print("================ Pipeline Complete ================\n")

if __name__ == "__main__":
    main()
