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

"""Tests for passata show."""

from tests.helpers import clipboard, run


def test_show(db):
    result = run(['show', 'internet/github'])
    assert result.output == (
        'password: gh\n'
        'username: takis\n'
    )


def test_show_nonexistent_entry(db):
    result = run(['show', 'internet/nonexistent'])
    assert isinstance(result.exception, SystemExit)
    assert result.output == "internet/nonexistent not found\n"


def test_show_entry_three_levels_deep(db):
    result = run(['show', 'one/two/three'])
    assert isinstance(result.exception, SystemExit)
    assert result.output == "one/two/three is nested too deeply\n"


def test_show_clipboard(db):
    result = run(['show', 'internet/github', '--clip'])
    assert result.output == ''
    assert clipboard() == 'gh'


def test_show_clipboard_whole_database(db):
    result = run(['show', '--clip'])
    assert isinstance(result.exception, SystemExit)
    assert result.output == "Can't put the entire database to clipboard\n"


def test_show_clipboard_whole_group(db):
    result = run(['show', 'internet', '--clip'])
    assert isinstance(result.exception, SystemExit)
    assert result.output == "Can't put the entire group to clipboard\n"


def test_show_group(db):
    result = run(['show', 'internet'])
    assert result.output == (
        'github:\n'
        '  password: gh\n'
        '  username: takis\n'
        'reddit:\n'
        '  password: rdt\n'
        '  username: sakis\n'
    )


def test_show_group_with_trailing_slash(db):
    result = run(['show', 'internet/'])
    assert result.output == (
        'github:\n'
        '  password: gh\n'
        '  username: takis\n'
        'reddit:\n'
        '  password: rdt\n'
        '  username: sakis\n'
    )


def test_show_color(db, editor):
    # Insert a new entry with a list
    editor(updated=(
        'username: user\n'
        'password: pass\n'
        'autotype: <username> Return !1.5 <password> Return\n'
        'keywords:\n'
        '- youtube\n'
        '- gmail\n'
    ))
    run(['edit', 'group/google'])

    # Test show without color
    expected = (
        'google:\n'
        '  username: user\n'
        '  password: pass\n'
        '  autotype: <username> Return !1.5 <password> Return\n'
        '  keywords:\n'
        '  - youtube\n'
        '  - gmail\n'
    )
    result = run(['--no-color', 'show', 'group'])
    assert result.output == expected

    # Test show with color
    expected = (
        '\033[38;5;12mgoogle\033[38;5;11m:\033[0m\n'
        '\033[38;5;12m  username\033[38;5;11m:\033[0m user\n'
        '\033[38;5;12m  password\033[38;5;11m:\033[0m pass\n'
        '\033[38;5;12m  autotype\033[38;5;11m:\033[0m '
        '<username> Return !1.5 <password> Return\n'
        '\033[38;5;12m  keywords\033[38;5;11m:\033[0m\n'
        '\033[38;5;9m  - \033[0myoutube\n'
        '\033[38;5;9m  - \033[0mgmail\n'
    )
    result = run(['--color', 'show', 'group'])
    assert result.output == expected
