#!/usr/bin/env python
#JSON {"lot": "UKS/6-31G(d)",
#JSON  "scf": "EDIIS2SCFSolver",
#JSON  "linalg": "CholeskyLinalgFactory",
#JSON  "difficulty": 5,
#JSON  "description": "Basic UKS DFT example with hyrbid GGA exhange-correlation functional (B3LYP)"}

from horton import *  # pylint: disable=wildcard-import,unused-wildcard-import


# Load the coordinates from file.
# Use the XYZ file from HORTON's test data directory.
fn_xyz = context.get_fn('test/methyl.xyz')
mol = IOData.from_file(fn_xyz)

# Create a Gaussian basis set
obasis = get_gobasis(mol.coordinates, mol.numbers, '6-31g(d)')

# Create a linalg factory
lf = DenseLinalgFactory(obasis.nbasis)

# Compute Gaussian integrals
olp = obasis.compute_overlap(lf)
kin = obasis.compute_kinetic(lf)
na = obasis.compute_nuclear_attraction(mol.coordinates, mol.pseudo_numbers, lf)
er = obasis.compute_electron_repulsion(lf)

# Define a numerical integration grid needed the XC functionals
grid = BeckeMolGrid(mol.coordinates, mol.numbers, mol.pseudo_numbers)

# Create alpha orbitals
exp_alpha = lf.create_expansion()
exp_beta = lf.create_expansion()

# Initial guess
guess_core_hamiltonian(olp, kin, na, exp_alpha, exp_beta)

# Construct the restricted HF effective Hamiltonian
external = {'nn': compute_nucnuc(mol.coordinates, mol.pseudo_numbers)}
libxc_term = ULibXCHybridGGA('xc_b3lyp')
terms = [
    UTwoIndexTerm(kin, 'kin'),
    UDirectTerm(er, 'hartree'),
    UGridGroup(obasis, grid, [libxc_term]),
    UExchangeTerm(er, 'x_hf', libxc_term.get_exx_fraction()),
    UTwoIndexTerm(na, 'ne'),
]
ham = UEffHam(terms, external)

# Decide how to occupy the orbitals (5 alpha electrons, 4 beta electrons)
occ_model = AufbauOccModel(5, 4)

# Converge WFN with CDIIS+EDIIS SCF
# - Construct the initial density matrix (needed for CDIIS+EDIIS).
occ_model.assign(exp_alpha, exp_beta)
dm_alpha = exp_alpha.to_dm()
dm_beta = exp_beta.to_dm()
# - SCF solver
scf_solver = EDIIS2SCFSolver(1e-6)
scf_solver(ham, lf, olp, occ_model, dm_alpha, dm_beta)

# Derive orbitals (coeffs, energies and occupations) from the Fock and density
# matrices. The energy is also computed to store it in the output file below.
fock_alpha = lf.create_two_index()
fock_beta = lf.create_two_index()
ham.reset(dm_alpha, dm_beta)
ham.compute_energy()
ham.compute_fock(fock_alpha, fock_beta)
exp_alpha.from_fock_and_dm(fock_alpha, dm_alpha, olp)
exp_beta.from_fock_and_dm(fock_beta, dm_beta, olp)

# Assign results to the molecule object and write it to a file, e.g. for
# later analysis. Note that the CDIIS+EDIIS algorithm can only really construct
# an optimized density matrix and no orbitals.
mol.title = 'UKS computation on methyl'
mol.energy = ham.cache['energy']
mol.obasis = obasis
mol.exp_alpha = exp_alpha
mol.exp_beta = exp_beta
mol.dm_alpha = dm_alpha
mol.dm_beta = dm_beta

# useful for post-processing (results stored in double precision):
mol.to_file('methyl.h5')

# CODE BELOW IS FOR horton-regression-test.py ONLY. IT IS NOT PART OF THE EXAMPLE.
rt_results = {
    'energy': ham.cache['energy'],
    'exp_alpha': exp_alpha.energies,
    'exp_beta': exp_beta.energies,
    'nn': ham.cache["energy_nn"],
    'kin': ham.cache["energy_kin"],
    'ne': ham.cache["energy_ne"],
    'grid': ham.cache["energy_grid_group"],
    'ex': ham.cache["energy_x_hf"],
    'hartree': ham.cache["energy_hartree"],
}
# BEGIN AUTOGENERATED CODE. DO NOT CHANGE MANUALLY.
import numpy as np  # pylint: disable=wrong-import-position
rt_previous = {
    'energy': -39.829219635738035,
    'ex': -1.2302245921907746,
    'exp_alpha': np.array([
        -10.202510805419273, -0.66406017496772685, -0.40272214145506163,
        -0.40271932405711497, -0.22486640330553606, 0.088865289955265131,
        0.16218818378752942, 0.16219513232872484, 0.53321762474455336, 0.5676983657643706,
        0.56770082505360386, 0.68335383164916741, 0.86349126731885351,
        0.86350325512698756, 0.9207151969432954, 1.6565381606272092, 1.6565783656997477,
        1.9537833876302899, 2.1093515670671379, 2.109434637212066
    ]),
    'exp_beta': np.array([
        -10.187835552622923, -0.62229231046907707, -0.39382059242599643,
        -0.393812529523204, -0.04712861670320255, 0.10635162807276623,
        0.16867798588387717, 0.16868833111894113, 0.57659434151316746,
        0.57660076741912725, 0.61221503662441623, 0.70335183838284976,
        0.86671222734246489, 0.86673750637878644, 0.95059963484638044, 1.7297544001544294,
        1.7299218939578214, 2.0444562761782712, 2.1211021738699447, 2.1211432410416582
    ]),
    'grid': -5.2062211181316655,
    'hartree': 28.101037319269153,
    'kin': 39.348971323946444,
    'ne': -109.92256751129483,
    'nn': 9.0797849426636361,
}
