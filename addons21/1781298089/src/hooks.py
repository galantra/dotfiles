# anki-search-inside-add-card
# Copyright (C) 2019 - 2020 Tom Z.

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import typing
from typing import Callable, Dict, Optional, Any

hooks       : Dict[str, Callable] = dict()
tmp_hooks   : Dict[str, Callable] = dict()

def add_hook(name: str, fn: Callable):
    name = name.lower()
    if name in hooks:
        hooks[name].append(fn)
    else:
        hooks[name] = [fn]

def add_tmp_hook(name: str, fn: Callable):
    """ This hook will be removed after one use. """
    name = name.lower()
    if name in tmp_hooks:
        tmp_hooks[name].append(fn)
    else:
        tmp_hooks[name] = [fn]


def run_hooks(name: str, arg: Optional[Any] = None):
    name = name.lower()
    if name in hooks:
        for fn in hooks[name]:
            if arg:
                try:
                    fn(arg)
                except:
                    fn()
            else:
                fn()
    if name in tmp_hooks:
        for fn in tmp_hooks[name]:
            if arg:
                try:
                    fn(arg)
                except:
                    fn()
            else:
                fn()
        del tmp_hooks[name]
