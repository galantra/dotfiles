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

import time
from aqt import mw
from .state import check_index
import typing
from typing import Callable

def perf_time(fn: Callable) -> Callable:
    """ Decorator to measure function execution time. """

    def _perf_wrapper(*args, **kwargs):
        start   = time.time() * 1000
        res     = fn(*args, **kwargs)
        print(f"{fn.__name__}: {time.time() * 1000 - start}")
        return res

    return _perf_wrapper

def js(fn: Callable) -> Callable:
    """ Decorator to execute the returned javascript of a function. """

    from .output import UI
    def _eval_js_dec(*args, **kwargs):
        if UI._editor is not None and UI._editor.web is not None:
            UI.js(fn(*args, **kwargs))
        else:
            w = mw.app.activeWindow()
            if w is not None and hasattr(w, "editor"):
                w.editor.web.eval(fn(*args, **kwargs))

    return _eval_js_dec

def requires_index_loaded(fn: Callable) -> Callable:
    """ Decorator to only enter a function if the index has been loaded. """

    def _check_ix(*args, **kwargs):
        if not check_index():
            return
        return fn(*args, **kwargs)

    return _check_ix


#
# Type Aliases
# 

HTML = str
JS   = str