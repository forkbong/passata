# Copyright 2017 Panagiotis Ktistakis <panktist@gmail.com>
#
# This file is part of passata.
#
# passata is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# passata is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with passata.  If not, see <http://www.gnu.org/licenses/>.

"""The passata test suite conftest file."""

import os

import pytest

import passata


@pytest.fixture
def db(tmpdir, monkeypatch):
    monkeypatch.setattr(passata, 'encrypt', lambda x: x)
    monkeypatch.setattr(passata, 'decrypt', lambda x: open(x).read())

    confpath = tmpdir.join('config.yml')
    dbpath = tmpdir.join('passata.db')

    confpath.write('database: %s\n'
                   'gpg_id: id\n' % dbpath)

    dbpath.write('internet:\n'
                 '  reddit:\n'
                 '    password: rdt\n'
                 '    username: sakis\n'
                 '  github:\n'
                 '    password: gh\n'
                 '    username: takis\n')

    os.environ['PASSATA_CONFIG_PATH'] = str(confpath)

    yield dbpath