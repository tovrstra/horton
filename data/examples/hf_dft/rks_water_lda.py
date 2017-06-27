#!/usr/bin/env python
#JSON {"lot": "RKS/6-31G(d)",
#JSON  "scf": "ODASCFSolver",
#JSON  "linalg": "CholeskyLinalgFactory",
#JSON  "difficulty": 3,
#JSON  "description": "Basic RKS DFT example with LDA exhange-correlation functional (Dirac+VWN)"}

from horton import *  # pylint: disable=wildcard-import,unused-wildcard-import


# Load the coordinates from file.
# Use the XYZ file from HORTON's test data directory.
fn_xyz = context.get_fn('test/water.xyz')
mol = IOData.from_file(fn_xyz)

# Create a Gaussian basis set
obasis = get_gobasis(mol.coordinates, mol.numbers, '6-31g(d)')

# Create a linalg factory
lf = CholeskyLinalgFactory(obasis.nbasis)

# Compute Gaussian integrals
olp = obasis.compute_overlap(lf)
kin = obasis.compute_kinetic(lf)
na = obasis.compute_nuclear_attraction(mol.coordinates, mol.pseudo_numbers, lf)
er = obasis.compute_electron_repulsion(lf)

# Define a numerical integration grid needed the XC functionals
grid = BeckeMolGrid(mol.coordinates, mol.numbers, mol.pseudo_numbers)

# Create alpha orbitals
exp_alpha = lf.create_expansion()

# Initial guess
guess_core_hamiltonian(olp, kin, na, exp_alpha)

# Construct the restricted HF effective Hamiltonian
external = {'nn': compute_nucnuc(mol.coordinates, mol.pseudo_numbers)}
terms = [
    RTwoIndexTerm(kin, 'kin'),
    RDirectTerm(er, 'hartree'),
    RGridGroup(obasis, grid, [
        RLibXCLDA('x'),
        RLibXCLDA('c_vwn'),
    ]),
    RTwoIndexTerm(na, 'ne'),
]
ham = REffHam(terms, external)

# Decide how to occupy the orbitals (5 alpha electrons)
occ_model = AufbauOccModel(5)

# Converge WFN with Optimal damping algorithm (ODA) SCF
# - Construct the initial density matrix (needed for ODA).
occ_model.assign(exp_alpha)
dm_alpha = exp_alpha.to_dm()
# - SCF solver
scf_solver = ODASCFSolver(1e-6)
scf_solver(ham, lf, olp, occ_model, dm_alpha)

# Derive orbitals (coeffs, energies and occupations) from the Fock and density
# matrices. The energy is also computed to store it in the output file below.
fock_alpha = lf.create_two_index()
ham.reset(dm_alpha)
ham.compute_energy()
ham.compute_fock(fock_alpha)
exp_alpha.from_fock_and_dm(fock_alpha, dm_alpha, olp)

# Assign results to the molecule object and write it to a file, e.g. for
# later analysis. Note that the ODA algorithm can only really construct an
# optimized density matrix and no orbitals.
mol.title = 'RKS computation on water'
mol.energy = ham.cache['energy']
mol.obasis = obasis
mol.exp_alpha = exp_alpha
mol.dm_alpha = dm_alpha

# useful for visualization:
mol.to_file('water.molden')
# useful for post-processing (results stored in double precision):
mol.to_file('water.h5')


# CODE BELOW IS FOR horton-regression-test.py ONLY. IT IS NOT PART OF THE EXAMPLE.
rt_results = {
    'energy': ham.cache['energy'],
    'exp_alpha': exp_alpha.energies,
    'nn': ham.cache["energy_nn"],
    'kin': ham.cache["energy_kin"],
    'ne': ham.cache["energy_ne"],
    'grid': ham.cache["energy_grid_group"],
    'hartree': ham.cache["energy_hartree"],
}
# BEGIN AUTOGENERATED CODE. DO NOT CHANGE MANUALLY.
import numpy as np  # pylint: disable=wrong-import-position
rt_previous = {
    'energy': -75.840489821694746,
    'exp_alpha': np.array([
        -18.58230481517597, -0.89645482184183045, -0.47394533974322334,
        -0.29938706464077286, -0.22841663753724872, 0.045271491553249367,
        0.12825353255457303, 0.76332895055364547, 0.80243034890203158,
        0.83062512325223159, 0.86463348691682496, 1.0042272336474725, 1.3160465964155548,
        1.6707142466917595, 1.6768134032677695, 1.718722082489359, 2.2334850292684449,
        2.520278714219923
    ]),
    'grid': -8.779901102250568,
    'hartree': 46.821068827153724,
    'kin': 75.86645763295653,
    'ne': -198.90529021598442,
    'nn': 9.1571750364299866,
}
