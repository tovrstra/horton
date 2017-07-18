// HORTON: Helpful Open-source Research TOol for N-fermion systems.
// Copyright (C) 2011-2017 The HORTON Development Team
//
// This file is part of HORTON.
//
// HORTON is free software; you can redistribute it and/or
// modify it under the terms of the GNU General Public License
// as published by the Free Software Foundation; either version 3
// of the License, or (at your option) any later version.
//
// HORTON is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program; if not, see <http://www.gnu.org/licenses/>
//
//--

// UPDATELIBDOCTITLE: Conversion of Cartesian to Pure Gaussian functions

#ifndef HORTON_GBASIS_CARTPURE_H_
#define HORTON_GBASIS_CARTPURE_H_

void cart_to_pure_low(double *work_cart, double *work_pure, long shell_type,
                      long nant, long npost);

#endif  // HORTON_GBASIS_CARTPURE_H_
