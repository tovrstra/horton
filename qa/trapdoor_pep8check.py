#!/usr/bin/env python
# -*- coding: utf-8 -*-
# HORTON: Helpful Open-source Research TOol for N-fermion systems.
# Copyright (C) 2011-2015 The HORTON Development Team
#
# This file is part of HORTON.
#
# HORTON is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# HORTON is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>
#
#--
'''Trapdoor test using pep8

   This test calls the pep8 program, see http://pep8.readthedocs.org/.
'''

import pep8
from collections import Counter
from trapdoor import main


def get_stats_pep8_check():
    '''Run tests using pep8

       Returns
       -------
       counter: collections.Counter
                counts for different error types in the current checkout
       messages: Set([]) of strings
                 all errors encountered in the current checkout
    '''
    pep8check = pep8.StyleGuide(reporter=CompleteReport, max_line_length=100)
    # pep8 check of horton directory
    pep8check.input_dir('horton')
    # counts of different errors
    counters = Counter(pep8check.options.report.counters)
    del counters['physical lines']
    del counters['logical lines']
    del counters['files']
    del counters['directories']
    # message on each error
    messages = set(pep8check.options.report.complete_message)
    assert len(messages) == pep8check.options.report.get_count()
    return counters, messages


class CompleteReport(pep8.StandardReport):
    '''
    Collect and record the results of the checks.
    '''
    def __init__(self, options):
        super(CompleteReport, self).__init__(options)
        self.complete_message = []

    def get_file_results(self):
        '''Record the result and return the overall count for this file.'''
        self._deferred_print.sort()
        for line_number, offset, code, text, doc in self._deferred_print:
            # record the error message specifications.
            message = '%15s  %50s  %s' % (
                code,
                ('%s:%s:%s' % (self.filename, self.line_offset + line_number, offset + 1)).ljust(50),
                text)
            if self._show_source:
                if line_number > len(self.lines):
                    line = ''
                else:
                    line = self.lines[line_number - 1]
            self.complete_message.append(message)


if __name__ == '__main__':
    main(get_stats_pep8_check)
