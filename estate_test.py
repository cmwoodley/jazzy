from jazzy.core import calculate_polar_strength_map
from jazzy.core import rdkit_molecule_from_smiles
from jazzy.core import kallisto_molecule_from_rdkit_molecule
from jazzy.core import get_covalent_atom_idxs
from jazzy.core import get_charges_from_kallisto_molecule
import numpy as np

smiles = "Fc1c(F)c(O)c(F)c(F)c1F"

rdkit_mol = rdkit_molecule_from_smiles(smiles, "MMFF94")
kmol = kallisto_molecule_from_rdkit_molecule(rdkit_mol)
atoms_and_nbrs = get_covalent_atom_idxs(rdkit_mol)
charges = get_charges_from_kallisto_molecule(kmol, 0)

map = calculate_polar_strength_map(rdkit_mol, kmol,atoms_and_nbrs, charges, m=0.5)

sa = [map[x]["sa"] for x in map.keys()]

print(sa)