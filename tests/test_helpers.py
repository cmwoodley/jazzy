"""Test cases for the helper methods."""
import numpy as np
import pytest

from jazzy.core import calculate_polar_strength_map
from jazzy.core import get_charges_from_kallisto_molecule
from jazzy.core import get_covalent_atom_idxs
from jazzy.core import kallisto_molecule_from_rdkit_molecule
from jazzy.core import rdkit_molecule_from_smiles
from jazzy.helpers import condense_atomic_map
from jazzy.helpers import convert_map_to_tuples
from jazzy.helpers import sum_atomic_map


def test_sum_atomic_map_fails_for_empty_map():
    """Correctly raise IndexError when atomic map is empty."""
    atomic_map = dict()
    with pytest.raises(IndexError) as error:
        sum_atomic_map(atomic_map)
    assert error.value.args[0] == "The atomic map must have length greater than zero."


def test_convert_map_to_tuples():
    """It creates correctly a list of tuples from a polar strength map."""
    smiles = "C1CC2=C3C(=CC=C2)C(=CN3C1)"
    rdkit_molecule = rdkit_molecule_from_smiles(smiles, minimisation_method="MMFF94")
    atoms_and_nbrs = get_covalent_atom_idxs(rdkit_molecule)
    kallisto_molecule = kallisto_molecule_from_rdkit_molecule(
        rdkit_molecule=rdkit_molecule
    )
    charge = 0
    eeq = get_charges_from_kallisto_molecule(kallisto_molecule, charge)
    mol_map = calculate_polar_strength_map(
        rdkit_molecule, kallisto_molecule, atoms_and_nbrs, eeq
    )
    tuple_map = convert_map_to_tuples(mol_map)
    assert tuple_map[0][0] == ("z", 6)
    assert tuple_map[0][1] == ("q", 0)
    assert tuple_map[0][2] == ("eeq", -0.1556)
    assert tuple_map[0][3] == ("alp", 7.4365)
    assert tuple_map[0][4] == ("hyb", "sp3")
    assert tuple_map[0][5] == ("num_lp", 0)
    assert tuple_map[0][6] == ("sdc", 0.0)
    assert tuple_map[0][7] == ("sdx", 0.0)
    assert tuple_map[0][8] == ("sa", 0.0)
    assert tuple_map[3][0] == ("z", 6)
    assert tuple_map[3][1] == ("q", 0)
    assert tuple_map[3][2] == ("eeq", 0.1174)
    assert tuple_map[3][3] == ("alp", 8.4498)
    assert tuple_map[3][4] == ("hyb", "sp2")
    assert tuple_map[3][5] == ("num_lp", 0)
    assert tuple_map[3][6] == ("sdc", 0.0)
    assert tuple_map[3][7] == ("sdx", 0.0)
    assert tuple_map[3][8] == ("sa", 0.0)


def test_convert_map_to_tuples_fails_for_empty_map():
    """It creates correctly a list of tuples from a polar strength map."""
    atomic_map = dict()
    with pytest.raises(Exception) as error:
        convert_map_to_tuples(atomic_map)
    assert error.value.args[0] == "The atomic map must have length greater than zero."


def test_condense_atomic_map():
    """It correctly condenses an atomic map."""
    smiles = "C1CC2=C3C(=CC=C2)C(=CN3C1)"
    rdkit_molecule = rdkit_molecule_from_smiles(smiles, minimisation_method="MMFF94")
    atoms_and_nbrs = get_covalent_atom_idxs(rdkit_molecule)
    kallisto_molecule = kallisto_molecule_from_rdkit_molecule(
        rdkit_molecule=rdkit_molecule
    )
    charge = 0
    eeq = get_charges_from_kallisto_molecule(kallisto_molecule, charge)
    mol_map = calculate_polar_strength_map(
        rdkit_molecule, kallisto_molecule, atoms_and_nbrs, eeq
    )
    condesed_map = condense_atomic_map(mol_map)
    assert np.isclose(condesed_map[0]["alp"], 7.4365)
    assert np.isclose(condesed_map[0]["eeq"], -0.1556)


def test_sum_atomic_map_acceptor_strengths():
    """Atomic acceptor strengths."""
    smiles = "CC(=O)NC1=CC=C(C=C1)O"
    rdkit_molecule = rdkit_molecule_from_smiles(smiles, minimisation_method="MMFF94")
    atoms_and_nbrs = get_covalent_atom_idxs(rdkit_molecule)
    kallisto_molecule = kallisto_molecule_from_rdkit_molecule(
        rdkit_molecule=rdkit_molecule
    )
    eeq = get_charges_from_kallisto_molecule(kallisto_molecule, 0)
    mol_map = calculate_polar_strength_map(
        rdkit_molecule, kallisto_molecule, atoms_and_nbrs, eeq
    )
    mol_vector = sum_atomic_map(mol_map)
    assert np.isclose(mol_vector["sa"], 2.5005)
