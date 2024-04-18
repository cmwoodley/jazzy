"""Test cases for the kallisto methods."""
import numpy as np
import pytest
from kallisto.units import Bohr
from rdkit import Chem
from rdkit.Chem.rdMolDescriptors import CalcNumAtoms
from tests.store import pyridine

from jazzy.core import get_charges_from_kallisto_molecule
from jazzy.core import kallisto_molecule_from_rdkit_molecule
from jazzy.core import rdkit_molecule_from_smiles
from jazzy.core import get_charges_by_method
from jazzy.exception import KallistoError


def test_kallisto_charges_are_correct_from_molecule():
    """It calculates the correct atomic EEQ partial charges."""
    want = [0.04352191, -0.0924591]
    # build molecule from store
    m = pyridine()
    charge = 0
    eeq = m.get_eeq(charge)
    assert np.isclose(eeq[0], want[0])
    assert np.isclose(eeq[1], want[1])


def test_kallisto_charges_are_correct_from_wrapper_function():
    """Calculate the correct atomic EEQ partial charges from wrapper."""
    want = [0.04352191, -0.0924591]
    # build molecule from store
    m = pyridine()
    charge = 0
    eeq = get_charges_from_kallisto_molecule(m, charge)
    assert np.isclose(eeq[0], want[0])
    assert np.isclose(eeq[1], want[1])


def test_kallisto_creation_fails_for_nonembedded_molecule() -> None:
    """It raises a KallistoError when a nonembedded molecule is entered."""
    with pytest.raises(KallistoError) as error:
        smiles = "CC"
        m = Chem.MolFromSmiles(smiles)
        kallisto_molecule_from_rdkit_molecule(m)
        assert (
            error.value.args[0]
            == "The kallisto molecule was not created for the input 'CC'"
        )


def test_kallisto_coordinates_match_rdkit_coordinates():
    """Both molecules have the same coordinates."""
    smiles = "C1CC2=C3C(=CC=C2)C(=CN3C1)"
    rdkit_molecule = rdkit_molecule_from_smiles(smiles=smiles)
    # get all xyz coordinates and split into list of lines
    xyz = Chem.rdmolfiles.MolToXYZBlock(rdkit_molecule).split("\n")
    # remove empty lines from list
    xyz = [line for line in xyz if line != ""]
    # remove number of atoms as given in xmol files (first line)
    xyz = xyz[1:]

    # create kallisto molecule
    kallisto_molecule = kallisto_molecule_from_rdkit_molecule(
        rdkit_molecule=rdkit_molecule
    )
    want = kallisto_molecule.get_positions()

    # check each coordinate
    for i, coord in enumerate(xyz):
        _, x, y, z = coord.split()[:4]
        position = [float(x) / Bohr, float(y) / Bohr, float(z) / Bohr]
        assert np.isclose(position[0], want[i][0])
        assert np.isclose(position[1], want[i][1])
        assert np.isclose(position[2], want[i][2])


def test_kallisto_from_rdkit_molecule_with_name():
    """A valid kallisto molecule is generated from an RDKit molecule with _Name."""
    # create rdkit molecule with a custom name
    smiles = "C1CC2=C3C(=CC=C2)C(=CN3C1)"
    rdkit_molecule = rdkit_molecule_from_smiles(smiles=smiles)
    rdkit_molecule.SetProp("_Name", "test1")

    # create kallisto molecule
    kallisto_molecule = kallisto_molecule_from_rdkit_molecule(
        rdkit_molecule=rdkit_molecule
    )

    # verify that molecule is created correctly
    rdkit_atoms = CalcNumAtoms(rdkit_molecule)
    kallisto_atoms = kallisto_molecule.get_number_of_atoms()
    assert rdkit_atoms == kallisto_atoms

def test_get_charges_by_method():
    smiles = "c1ccccn1" # Pyridine
    rdkit_molecule = rdkit_molecule_from_smiles(smiles, minimisation_method="MMFF94")
    kallisto_molecule = kallisto_molecule_from_rdkit_molecule(rdkit_molecule)
    charge_method = "kallisto"
    want = [0.045680464157738396, -0.0957233733338991, -0.09286581882421709, -0.09572340650673523, 0.045680551016580355, -0.38330394049694483, 0.12270838091939198, 0.10919952318565886, 0.11243965258629614, 0.10919954271115259, 0.1227084245849779]
    got = get_charges_by_method(rdkit_molecule, kallisto_molecule, charge_method)
    assert np.isclose(got[0], want[0])
    assert np.isclose(got[1], want[1])
    assert np.isclose(got[2], want[2])

    charge_method = "MMFF94"
    want = [0.16, -0.15, -0.15, -0.15, 0.16, -0.62, 0.15, 0.15, 0.15, 0.15, 0.15]
    got = get_charges_by_method(rdkit_molecule, kallisto_molecule, charge_method)
    assert np.isclose(got[0], want[0])
    assert np.isclose(got[1], want[1])
    assert np.isclose(got[2], want[2])

def test_get_charges_by_method_invalid_method():
    """It exits with a ValueError when a nonvalid method is entered."""
    with pytest.raises(Exception) as error:
        smiles = "CC"
        charge_method = "MMFF95"
        rdkit_molecule = rdkit_molecule_from_smiles(smiles, minimisation_method="MMFF94")
        kallisto_molecule = kallisto_molecule_from_rdkit_molecule(rdkit_molecule)
        charges = get_charges_by_method(rdkit_molecule, kallisto_molecule, charge_method)
    assert error.value.args[0] == "Select a valid charge calculation method ['kallisto', 'MMFF94']"
