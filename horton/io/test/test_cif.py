# -*- coding: utf-8 -*-
# Horton is a Density Functional Theory program.
# Copyright (C) 2011-2013 Toon Verstraelen <Toon.Verstraelen@UGent.be>
#
# This file is part of Horton.
#
# Horton is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# Horton is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>
#
#--


import h5py as h5, tempfile, shutil

from horton import *
from horton.io.cif import _load_cif_low

from horton.test.common import compare_symmetries


lta_sep = np.array([
    '+x,+y,+z', '+z,+x,+y', '+y,+z,+x', '+x,+y,-z', '+z,+x,-y', '+y,+z,-x',
    '-x,+y,+z', '-z,+x,+y', '-y,+z,+x', '-x,+y,-z', '-z,+x,-y', '-y,+z,-x',
    '+y,+x,+z', '+x,+z,+y', '+z,+y,+x', '+y,+x,-z', '+x,+z,-y', '+z,+y,-x',
    '+y,-x,+z', '+x,-z,+y', '+z,-y,+x', '+y,-x,-z', '+x,-z,-y', '+z,-y,-x',
    '-x,-y,-z', '-z,-x,-y', '-y,-z,-x', '-x,-y,+z', '-z,-x,+y', '-y,-z,+x',
    '+x,-y,-z', '+z,-x,-y', '+y,-z,-x', '+x,-y,+z', '+z,-x,+y', '+y,-z,+x',
    '-y,-x,-z', '-x,-z,-y', '-z,-y,-x', '-y,-x,+z', '-x,-z,+y', '-z,-y,+x',
    '-y,+x,-z', '-x,+z,-y', '-z,+y,-x', '-y,+x,+z', '-x,+z,+y', '-z,+y,+x'
])

lta_sep_strip = np.array([
    'x,y,z', '-x,-y,z', '-x,y,-z', 'x,-y,-z', 'z,x,y', 'z,-x,-y', '-z,-x,y',
    '-z,x,-y', 'y,z,x', '-y,z,-x', 'y,-z,-x', '-y,-z,x', 'y,x,-z', '-y,-x,-z',
    'y,-x,z', '-y,x,z', 'x,z,-y', '-x,z,y', '-x,-z,-y', 'x,-z,y', 'z,y,-x',
    'z,-y,x', '-z,y,x', '-z,-y,-x', '-x,-y,-z', 'x,y,-z', 'x,-y,z', '-x,y,z',
    '-z,-x,-y', '-z,x,y', 'z,x,-y', 'z,-x,y', '-y,-z,-x', 'y,-z,x', '-y,z,x',
    'y,z,-x', '-y,-x,z', 'y,x,z', '-y,x,-z', 'y,-x,-z', '-x,-z,y', 'x,-z,-y',
    'x,z,y', '-x,z,-y', '-z,-y,x', '-z,y,-x', 'z,-y,-x', 'z,y,x'
])


def test_load_cif_low_lta_castep():
    title, fields = _load_cif_low(context.get_fn('test/lta_castep.cif'))
    assert title == 'LTA_CASTEP'
    assert fields['audit_creation_date'] == '02:54:15 (GMT+0.0) 29th November 2012'
    assert fields['audit_creation_method'] == 'Generated by CASTEP  5.501'
    assert (fields['symmetry_equiv_pos_as_xyz'] == lta_sep_strip).all()
    assert fields['cell_length_a'] == 12.023414845123691
    assert fields['cell_length_b'] == 12.023414845123691
    assert fields['cell_length_c'] == 12.023414845123691
    assert fields['cell_angle_alpha'] == 90.0
    assert fields['cell_angle_beta'] == 90.0
    assert fields['cell_angle_gamma'] == 90.0
    assert (fields['atom_site_label'] == ['O1', 'O13', 'O25', 'Si1']).all()
    assert (fields['atom_site_fract_x'] == [-1.220667052947635, -0.292509343078465, -1.110956438805889, -1.183699077638015]).all()
    assert (fields['atom_site_fract_y'] == [1.0, 1.0, 1.110956438805889, 1.0]).all()
    assert (fields['atom_site_fract_z'] == [0.5, 1.292509343078465, 0.345757991600433, 0.370366544189800]).all()
    assert (fields['atom_site_U_iso_or_equiv'] == 0.0100).all()
    assert fields['atom_site_U_iso_or_equiv'].shape == (4,)
    assert (fields['atom_site_occupancy'] == 1.0).all()
    assert fields['atom_site_occupancy'].shape == (4,)
    assert len(fields) == 15


def test_load_cif_low_lta_gulp():
    title, fields = _load_cif_low(context.get_fn('test/lta_gulp.cif'))
    assert title == 'LTA_min'
    assert fields['audit_creation_date'] == '2012-11-28'
    assert fields['audit_creation_method'] == 'Materials Studio'
    assert fields['symmetry_space_group_name_H-M'] == 'PM-3M'
    assert fields['symmetry_Int_Tables_number'] == 221
    assert isinstance(fields['symmetry_Int_Tables_number'], int)
    assert fields['symmetry_cell_setting'] == 'cubic'
    assert (fields['symmetry_equiv_pos_as_xyz'] == lta_sep_strip).all()
    assert fields['cell_length_a'] == 11.8278
    assert fields['cell_length_b'] == 11.8278
    assert fields['cell_length_c'] == 11.8278
    assert fields['cell_angle_alpha'] == 90.0
    assert fields['cell_angle_beta'] == 90.0
    assert fields['cell_angle_gamma'] == 90.0
    assert (fields['atom_site_label'] == ['Si1', 'O2', 'O3', 'O4']).all()
    assert (fields['atom_site_type_symbol'] == ['Si', 'O', 'O', 'O']).all()
    assert (fields['atom_site_fract_x'] == [-1.18386, -1.22031, -0.29671, -1.11082]).all()
    assert (fields['atom_site_fract_y'] == [1.0, 1.0, 1.0, 1.11082]).all()
    assert (fields['atom_site_fract_z'] == [0.36956, 0.50000, 1.29671, 0.34116]).all()
    assert (fields['atom_site_U_iso_or_equiv'] == 0.0).all()
    assert (fields['atom_site_adp_type'] == 'Uiso').all()
    assert (fields['atom_site_occupancy'] == 1.0).all()
    assert len(fields) == 20


def test_load_cif_low_lta_iza():
    title, fields = _load_cif_low(context.get_fn('test/lta_iza.cif'))
    assert title == 'LTA'
    assert fields['cell_length_a'] == 11.9190
    assert fields['cell_length_b'] == 11.9190
    assert fields['cell_length_c'] == 11.9190
    assert fields['cell_angle_alpha'] == 90.0
    assert fields['cell_angle_beta'] == 90.0
    assert fields['cell_angle_gamma'] == 90.0
    assert (fields['symmetry_equiv_pos_as_xyz'] == lta_sep).all()
    assert fields['symmetry_space_group_name_H-M'] == 'P m 3 m'
    assert fields['symmetry_Int_Tables_number'] == 221
    assert fields['symmetry_cell_setting'] == 'cubic'
    assert (fields['atom_site_label'] == ['O1', 'O2', 'O3', 'Si']).all()
    assert (fields['atom_site_type_symbol'] == ['O', 'O', 'O', 'Si']).all()
    assert (fields['atom_site_fract_x'] == [0.0, 0.1103, 0.0, 0.0]).all()
    assert (fields['atom_site_fract_y'] == [0.2122, 0.1103, 0.2967, 0.1823]).all()
    assert (fields['atom_site_fract_z'] == [0.5, 0.3384, 0.2967, 0.3684]).all()
    assert len(fields) == 15


def test_iter_equiv_pos_terms():
    assert list(iter_equiv_pos_terms('x+1/2')) == [(+1,'x'),(+1,'1/2')]
    assert list(iter_equiv_pos_terms('-x+1/2')) == [(-1,'x'),(+1,'1/2')]
    assert list(iter_equiv_pos_terms('y-1/2')) == [(+1,'y'),(-1,'1/2')]
    assert list(iter_equiv_pos_terms('z')) == [(+1,'z')]


def test_equiv_pos_to_generator():
    assert abs(equiv_pos_to_generator('x,y,z') - np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0]])).max() < 1e-10
    assert abs(equiv_pos_to_generator('y,x,z') - np.array([[0,1,0,0],[1,0,0,0],[0,0,1,0]])).max() < 1e-10
    assert abs(equiv_pos_to_generator('y,z,x') - np.array([[0,1,0,0],[0,0,1,0],[1,0,0,0]])).max() < 1e-10
    assert abs(equiv_pos_to_generator('x,-y,-z') - np.array([[1,0,0,0],[0,-1,0,0],[0,0,-1,0]])).max() < 1e-10
    assert abs(equiv_pos_to_generator('-y,z,x') - np.array([[0,-1,0,0],[0,0,1,0],[1,0,0,0]])).max() < 1e-10
    assert abs(equiv_pos_to_generator('x+1/2,y,z') - np.array([[1,0,0,0.5],[0,1,0,0],[0,0,1,0]])).max() < 1e-10
    assert abs(equiv_pos_to_generator('x,y-3/4,z') - np.array([[1,0,0,0],[0,1,0,-0.75],[0,0,1,0]])).max() < 1e-10


def check_lta_sys(sys):
    assert (sys.numbers == 14).sum() == 24
    assert (sys.numbers == 8).sum() == 48
    assert sys.props['symmetry'].name == '221'
    assert len(sys.props['links']) == 72


def test_load_cif_lta_gulp():
    sys = System.from_file(context.get_fn('test/lta_gulp.cif'))
    check_lta_sys(sys)


def test_load_cif_lta_iza():
    sys = System.from_file(context.get_fn('test/lta_iza.cif'))
    check_lta_sys(sys)


def test_checkpoint():
    with h5.File('horton.io.test.test_cif.test_checkpoint', driver='core', backing_store=False) as f:
        sys0 = System.from_file(context.get_fn('test/lta_iza.cif'))
        sys0.to_file(f)
        sys1 = System.from_file(f)
        s0 = sys0.props['symmetry']
        s1 = sys1.props['symmetry']
        compare_symmetries(s0, s1)


def test_dump_load_consistency():
    sys0 = System.from_file(context.get_fn('test/aelta.cube'))
    tmpdir = tempfile.mkdtemp('horton.io.test.test_cif.test_dump_load_consistency')
    fn_cif = '%s/test.cif' % tmpdir
    try:
        sys0.to_file(fn_cif)
        sys1 = System.from_file(fn_cif)
    finally:
        shutil.rmtree(tmpdir)

    assert sys0.cell.nvec == sys1.cell.nvec
    lengths0, angles0 = sys0.cell.parameters
    lengths1, angles1 = sys1.cell.parameters
    assert abs(lengths0 - lengths1).max() < 1e-6
    assert abs(angles0 - angles1).max() < 1e-6
    assert (sys0.numbers == sys1.numbers).all()
    frac0 = np.array([sys0.cell.to_frac(row) for row in sys0.coordinates])
    frac1 = np.array([sys1.cell.to_frac(row) for row in sys1.coordinates])
    assert abs(frac0 - frac1).max() < 1e-6
