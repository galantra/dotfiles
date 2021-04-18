"""
Anki Add-on "Extended tag add/edit dialog"

Copyright (c): 2019- ijgnd

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.



This add-on uses the file fuzzy_panel.py which has this copyright and permission notice:

    Copyright (c): 2018  Rene Schallner
                   2019- ijgnd
        
    This file (fuzzy_panel.py) is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This file is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this file.  If not, see <http://www.gnu.org/licenses/>.
"""

import os

from anki.lang import _
from anki.hooks import addHook, wrap

from aqt import mw
from aqt.addcards import AddCards
from aqt.editcurrent import EditCurrent
from aqt.editor import Editor
from aqt.browser import Browser
from aqt.tagedit import TagEdit
from aqt.utils import (
    getTag, 
    saveGeom,
    restoreGeom,
    # shortcut,
    showInfo,
    tooltip,
)
from aqt.qt import *
from aqt.reviewer import Reviewer

from .fuzzy_panel import FilterDialog


def gc(arg, fail=False):
    conf = mw.addonManager.getConfig(__name__)
    if conf:
        return conf.get(arg, fail)
    else:
        return fail


# startup warning for 2020-06-09
addon_path = os.path.dirname(__file__)
user_files_folder = os.path.join(addon_path, "user_files")
message_2020_06_update = os.path.join(user_files_folder, "message_2020_06_update_shown")

# I can't rely on detecting old config keys from meta.json: If the user never changed the config
# the old config is not in meta.json but it's completely lost after an update.
if not os.path.isfile(message_2020_06_update):
    addonname = "Extended Tag Add/Edit Dialog"
    msg = (f"""
This is an infobox from the add-on "<b>{addonname}</b>".
<br><br>
It's shown one time because you just installed it or just upgraded. If you just installed this 
add-on for the first time the rest of this message is not very relevant for you.
<br><br>
The latest upgrade from 2020-06-30 changed all shortcuts and their names for this add-on.
<br><br>
The default shortcut to open the extended tag edit dialog is now "Ctrl+t, d": You press "Ctrl+t", 
then release both keys and then press "d". On MacOS instead of "Ctrl+t" you use "Cmd+t".
<br><br>
The default shortcut to add a single tag in the editor changed to "Ctrl+t, a".
<br><br>
There are two reasons for this change: I can remember these shortcuts more easily because 
for "Ctrl+<i>t</i>, <i>d</i>" I use the mnemonic "<i>t</i>ag-<i>d</i>ialog" and for 
"Ctrl+<i>t</i>, <i>a</i>" the mnemonic is "<i>t</i>ag-<i>a</i>dd". Also this add-on is often used 
together with the add-on <a href="https://ankiweb.net/shared/info/1918380616">High Yield Tags</a> 
which in the most recent version from 2020-06-30 changed to similar shortcuts.
<br><br>
This upgrade also has some improvements like Ctrl+N/Ctrl+P to switch beween the lines 
of my extended tag dialog. 
<br><br>The old settings no longer work. If you had a custom config you should reset the config 
to remove old config keys that are no longer used and then adjust the config to your needs with your 
custom shortcuts.
"""
    )
    showInfo(msg, textFormat="rich")
    if not os.path.isdir(user_files_folder):
        os.makedirs(user_files_folder)
    open(message_2020_06_update, 'a').close()


def tagselector(self):
    alltags = self.col.tags.all()
    d = FilterDialog(parent=self, values=alltags, allownew=True)
    if d.exec():
        # self.setText(self.text() + " " + d.selkey)
        # order and remove duplicates 
        tags = mw.col.tags.split(self.text() + " " + d.selkey)
        uniquetags = list(set(tags))
        self.setText(mw.col.tags.join(mw.col.tags.canonify(uniquetags))) 
TagEdit.tagselector = tagselector


def myinit(self, parent, type=0):
    self.parent = parent
    cut = gc("editor: show filterdialog to add single tag")
    if cut:
        if hasattr(self, "isMyTagEdit") and self.isMyTagEdit:
            return
        # doesn't work in extended dialog since there are multiple TagEdits
        self.tagselector_cut = QShortcut(QKeySequence(cut), self)
        self.tagselector_cut.activated.connect(self.tagselector)
TagEdit.__init__ = wrap(TagEdit.__init__, myinit)


class MyTagEdit(TagEdit):
    def __init__(self, parent, type=0):
        super().__init__(parent, type=0)
        self.isMyTagEdit = True

    def keyPressEvent(self, evt):
        modctrl = evt.modifiers() & Qt.ControlModifier 
        sp = gc("tag dialog space")
        if evt.key() == Qt.Key_Space:
            if sp:
                if sp.lower() in ["return", "enter"]:
                    sp = Qt.Key_Space
                else:
                    self.setText(self.text() + sp)
                    return
            else:
                sp = Qt.Key_Space
        if evt.key() in (sp, Qt.Key_Enter, Qt.Key_Return, Qt.Key_Tab):
            if (evt.key() == Qt.Key_Tab and evt.modifiers() & Qt.ControlModifier):
                super().keyPressEvent(evt)
            else:
                selected_row = self.completer.popup().currentIndex().row()
                if selected_row == -1:
                    self.completer.setCurrentRow(0)
                    index = self.completer.currentIndex()
                    self.completer.popup().setCurrentIndex(index)
                self.hideCompleter()
                # QWidget.keyPressEvent(self, evt)
                self.parent.addline()
                return
        elif (evt.key() == Qt.Key_Up) or (modctrl and evt.key() == Qt.Key_P):
            self.parent.change_focus_by_one(False)
            return
        elif (evt.key() == Qt.Key_Down) or (modctrl and evt.key() == Qt.Key_N):
            self.parent.change_focus_by_one()
            return
        else:
            super().keyPressEvent(evt)


focused_line = None


class MyBasicEdit(QLineEdit):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.isMyTagEdit = False

    def focusInEvent(self, event):
        global focused_line
        focused_line = self
        super().focusInEvent(event)

    def keyPressEvent(self, evt):
        modctrl = evt.modifiers() & Qt.ControlModifier
        sp = None # gc("tag dialog space")
        if evt.key() == Qt.Key_Space:
            if sp:
                if sp.lower() in ["return", "enter"]:
                    sp = Qt.Key_Space
                else:
                    self.setText(self.text() + sp)
                    return
            else:
                sp = Qt.Key_Space
        if evt.key() in (sp, Qt.Key_Enter, Qt.Key_Return, Qt.Key_Tab):
            if (evt.key() == Qt.Key_Tab and modctrl):
                super().keyPressEvent(evt)
            else:
                self.parent.addline()
                return
        elif (evt.key() == Qt.Key_Up) or (modctrl and evt.key() == Qt.Key_P):
            self.parent.change_focus_by_one(False)
            return
        elif (evt.key() == Qt.Key_Down) or (modctrl and evt.key() == Qt.Key_N):
            self.parent.change_focus_by_one()
            return
        else:
            super().keyPressEvent(evt)


class TagDialogExtended(QDialog):
    def __init__(self, parent, tags, alltags):
        QDialog.__init__(self, parent, Qt.Window)  # super().__init__(parent)
        self.basic_mode = gc("basic_but_quick")
        self.parent = parent
        self.alltags = alltags
        self.gridLayout = QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QLabel("Edit tags:")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout.addLayout(self.verticalLayout, 1, 0, 1, 1)
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.shortcut = QShortcut(QKeySequence("Ctrl+Return"), self)
        self.shortcut.activated.connect(self.accept)
        self.helpButton = QPushButton("add empty line", clicked=lambda: self.addline(force=True))
        self.buttonBox.addButton(self.helpButton, QDialogButtonBox.HelpRole)
        self.filterbutton = QPushButton("edit tag for current line", clicked=self.tagselector)
        self.buttonBox.addButton(self.filterbutton, QDialogButtonBox.ResetRole)
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 1)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.setWindowTitle("Anki - Edit Tags")
        originalheight = self.height()
        restoreGeom(self, "TagDialogExtended")
        self.resize(self.width(), originalheight)
        if not tags:
            tags = ["",]
        else:
            tags.append("")
        self.line_list = []
        for t in tags:
            self.addline(t)
        self.cut = gc("in tag lines dialog: open filterdialog for single tag")
        if self.cut:
            self.filterbutton.setToolTip('shortcut: {}'.format(self.cut))
            self.selkey = QShortcut(QKeySequence(self.cut), self)
            self.selkey.activated.connect(self.tagselector)  #self.focus_three) #
        # don't also set Ctrl+t,a/gc("editor: show filterdialog to add single tag") for 
        # self.tagselector: What if the user has already set them to the same etc. I'd have
        # to do a lot of checking
        self.addnl = gc("in tag lines dialog: insert additional line")
        if self.addnl:
            self.helpButton.setToolTip('shortcut: {}'.format(self.addnl))
            self.addnlscut = QShortcut(QKeySequence(self.addnl), self)
            self.addnlscut.activated.connect(lambda: self.addline(force=True))       

    def tagselector(self):
        text = focused_line.text()
        d = FilterDialog(parent=self, values=self.alltags, allownew=True, prefill=text)
        if d.exec():
            focused_line.setText(d.selkey)
        else:
            focused_line.setFocus()

    def change_focus_by_one(self, Down=True):
        for index, edit in enumerate(self.line_list):
            if edit == focused_line:
                if Down:
                    if index == len(self.line_list)-1:  # if in last line go up
                        self.line_list[0].setFocus()
                        break
                    else:
                        newidx = index+1
                        self.line_list[newidx].setFocus()
                        break
                else:  # go up
                    if index == 0:  # if in last line go up
                        newidx = len(self.line_list)-1
                        self.line_list[newidx].setFocus()
                        break
                    else:
                        self.line_list[index-1].setFocus()
                        break

    def addline(self, tag="", force=False):
        if self.line_list and not self.line_list[-1].text() and not force:  # last lineedit is empty:
            self.line_list[-1].setFocus()
            self.line_list[-1].setText(tag)
        else:
            if self.basic_mode:
                te = MyBasicEdit(self)
                te.setText(tag)
                self.verticalLayout.addWidget(te)
                te.setFocus()
                self.line_list.append(te)
            else:
                te = MyTagEdit(self)
                te.setCol(mw.col)
                te.setText(tag)
                self.verticalLayout.addWidget(te)
                te.hideCompleter()
                te.setFocus()
                self.line_list.append(te)

    def accept(self):
        self.tagstring = ""
        for t in self.line_list:
            if not self.basic_mode:
                t.hideCompleter()
            text = t.text()
            if text:
                self.tagstring += text + " "
        saveGeom(self, "TagDialogExtended")
        QDialog.accept(self)

    def reject(self):
        saveGeom(self, "TagDialogExtended")
        QDialog.reject(self)


#### Browser/Editor
def edit_tag_dialogFromEditor(editor):
    fi = editor.currentField
    editor.saveNow(lambda e=editor, i=fi: _edit_tag_dialogFromEditor(e, i))
Editor.edit_tag_dialogFromEditor = edit_tag_dialogFromEditor


def _edit_tag_dialogFromEditor(editor, index):
    mw.checkpoint(_("Edit Tags"))
    note = editor.note
    alltags = mw.col.tags.all()
    d = TagDialogExtended(editor.parentWindow, note.tags, alltags)
    if not d.exec():
        return
    tagString = d.tagstring
    note.setTagsFromStr(tagString)
    if not editor.addMode:
        note.flush()
    addmode = editor.addMode
    editor.addMode = False
    tooltip('Edited tags "%s"' % tagString)
    editor.loadNote(focusTo=index)
    editor.addMode = addmode


# addHook("setupEditorShortcuts", SetupShortcuts) doesn't work when editor is not focused, e.g.
# if focus is on tag line. So using an editor shortcut here is bad.
def addAddshortcut(self, mw):
    cut = gc("open tag lines dialog: from editor")
    if cut:
        shortcut = QShortcut(QKeySequence(cut), self)
        shortcut.activated.connect(self.editor.edit_tag_dialogFromEditor)
AddCards.__init__ = wrap(AddCards.__init__, addAddshortcut)
EditCurrent.__init__ = wrap(EditCurrent.__init__, addAddshortcut)


def EditorContextMenu(view, menu):
    a = menu.addAction('edit tags')
    a.triggered.connect(lambda _, e=view.editor: edit_tag_dialogFromEditor(e))
addHook("EditorWebView.contextMenuEvent", EditorContextMenu)


# allow to clone from the browser table (when you are not in the editor)
def browser_edit_tags(browser):
    if len(browser.selectedCards()) == 1:
        return edit_tag_dialogFromEditor(browser.editor)
    tooltip("only works if one card is selected")


def setupMenu(browser):
    global myaction
    myaction = QAction(browser)
    myaction.setText("edit tags")
    cut = gc("open tag lines dialog: from editor", False)
    if cut:
        myaction.setShortcut(QKeySequence(cut))
    myaction.triggered.connect(lambda _, b=browser: browser_edit_tags(b))
    browser.form.menuEdit.addAction(myaction)
addHook("browser.setupMenus", setupMenu)


def add_to_table_context_menu(browser, menu):
    menu.addAction(myaction)
#addHook("browser.onContextMenu", add_to_table_context_menu)


def edit_tag_dialogFromReviewer():
    mw.checkpoint(_("Edit Tags"))
    note = mw.reviewer.card.note()
    alltags = mw.col.tags.all()
    d = TagDialogExtended(mw, note.tags, alltags)
    if not d.exec():
        return
    tagString = d.tagstring
    note.setTagsFromStr(tagString)
    note.flush()
    tooltip('Edited tags "%s"' % tagString)


def addShortcuts(cuts):
    cuts.append((gc("open tag lines dialog: from reviewer", "w"), edit_tag_dialogFromReviewer))
addHook("reviewStateShortcuts", addShortcuts)


def ReviewerContextMenu(view, menu):
    if mw.state != "review":
        return
    a = menu.addAction('edit tags (shorcut: {})'.format(gc("open tag lines dialog: from reviewer", "w")))
    a.triggered.connect(edit_tag_dialogFromReviewer)
addHook("AnkiWebView.contextMenuEvent", ReviewerContextMenu)
