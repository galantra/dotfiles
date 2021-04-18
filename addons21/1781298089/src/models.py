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

import utility.text
import utility.misc
import html
import re
import typing
from typing import Tuple, List, Any, Optional

from datetime import datetime, timedelta
from .web_import import import_webpage
from .config import get_config_value_or_default
from .markdown import markdown
from .markdown.extensions.fenced_code import FencedCodeExtension
from .markdown.extensions.def_list import DefListExtension

DUE_NOTES_BOUNDARY = get_config_value_or_default("notes.queue.due_note_boundary", 7)

class Printable():

    def get_content(self) -> str:
        """
        Should return the "body" of the note, e.g. the 'source' field in case of index notes and the
        'text' field in case of SiacNote.
        """
        raise NotImplementedError()

class SiacNote(Printable):

    _ct_timestamp   = 0
    note_type       = "user"

    # 2020-10-06 Simplify scheduling
    # MISSED_NOTES    = get_config_value_or_default("notes.queue.missedNotesHandling", "remove-schedule")
    MISSED_NOTES    = "place-front"

    def __init__(self, props: Tuple[Any, ...]):
        self.id             : int           = props[0]
        self.title          : str           = props[1]
        self.text           : str           = props[2]
        self.source         : str           = props[3]
        self.tags           : str           = props[4]
        self.nid            : int           = props[5]
        self.created        : str           = props[6]
        self.modified       : str           = props[7]
        self.reminder       : str           = props[8]
        self.lastscheduled  : str           = props[9]
        self.position       : int           = props[10]
        self.extract_start  : Optional[int] = props[11]
        self.extract_end    : Optional[int] = props[12]
        self.delay          : Optional[str] = props[13]
        self.author         : str           = props[14]
        self.priority       : float         = props[15]
        self.last_priority  : float         = props[16]
        self.url            : str           = props[17]

        self.mid            : int = -1

    @staticmethod
    def from_index(index_props: Tuple[Any, ...]) -> 'SiacNote':

        id      = int(index_props[0])
        # if the note was stored in the index, its title, text, and source fields are collapsed into a single field, separated by \u001f
        text    = index_props[4]
        title   = text.split("\u001f")[0]
        body    = text.split("\u001f")[1]
        src     = text.split("\u001f")[2]

        return SiacNote((id, title, body, src, index_props[2], -1, "", "", "", "", -1, None, None, None, None, None, None, None))

    @staticmethod
    def mock(title: str, body: str, tags: str) -> 'SiacNote':
        """ Used to create a 'mock' SiacNote object, that is not linked to an entity in the DB. """

        SiacNote._ct_timestamp += 1
        id = - (utility.misc.get_milisec_stamp() + SiacNote._ct_timestamp)
        return SiacNote((id, title, body, "", tags, -1, "", "", "", "", -1, None, None, None, None, None, None, None))

    def get_content(self) -> str:
        return self._build_non_anki_note_html()

    def is_pdf(self) -> bool:
        if self.is_file():
            return False
        return self.source is not None and self.source.strip().lower().endswith(".pdf")

    def is_file(self) -> bool:
        if self.is_yt():
            return False
        return self.source is not None and re.match("^(?:\\S+):///", self.source.strip().lower())

    def is_feed(self) -> bool:
        return self.source is not None and self.source.strip().lower().startswith("feed:")

    def is_yt(self) -> bool:
        return self.source is not None and re.match("(?:https?://)?www\.youtube\..+", self.source.strip().lower())
    
    def is_md(self) -> bool:
        return self.source is not None and self.source.lower().startswith("md:///")

    def get_note_type(self) -> str:
        if self.is_pdf():
            return "PDF"
        if self.is_yt():
            return "Video"
        return "Text"

    def is_in_queue(self) -> bool:
        return self.position is not None and self.position >= 0

    def get_title(self) -> str:
        if self.title is None or len(self.title.strip()) == 0:
            return "Untitled"
        return self.title

    def get_containing_folder(self) -> Optional[str]:
        if not self.is_pdf():
            return None
        source = self.source[:self.source.rindex("/")]
        return source

    def is_due_today(self) -> bool:
        if not self.has_schedule():
            return False
        dt = datetime.strptime(self.reminder.split("|")[1], '%Y-%m-%d-%H-%M-%S')
        return dt.date() == datetime.today().date()

    def has_schedule(self) -> bool:
        if self.reminder is None or len(self.reminder.strip()) == 0 or not "|" in self.reminder:
            return False
        return True

    def is_due_in_future(self) -> bool:
        return self.has_schedule() and utility.date.schedule_is_due_in_the_future(self.reminder)

    def is_scheduled(self) -> bool:
        if self.reminder is None or len(self.reminder.strip()) == 0 or not "|" in self.reminder:
            return False
        if SiacNote.MISSED_NOTES != "place-front":
            return self.is_due_today()
        return self.is_or_was_due()

    def is_or_was_due(self) -> bool:
        if not self.has_schedule():
            return False
        dt = datetime.strptime(self.reminder.split("|")[1], '%Y-%m-%d-%H-%M-%S')
        return dt.date() >= (datetime.today()  - timedelta(days=DUE_NOTES_BOUNDARY)).date() and dt.date() <= datetime.today().date()

    def is_due_sometime(self) -> bool:
        return self.has_schedule()

    def due_date_str(self) -> Optional[str]:
        if self.reminder is None or len(self.reminder.strip()) == 0 or not "|" in self.reminder:
            return None
        return self.current_due_date().strftime('%Y-%m-%d')

    def current_due_date(self) -> Optional[datetime]:
        if not self.is_due_sometime():
            return None
        return datetime.strptime(self.reminder.split("|")[1], '%Y-%m-%d-%H-%M-%S')

    def due_days_delta(self) -> int:
        return (datetime.now().date() - self.current_due_date().date()).days

    def schedule_type(self) -> str:
        return self.reminder.split("|")[2][:2]

    def schedule_value(self) -> str:
        return self.reminder.split("|")[2][3:]

    def is_meta_note(self) -> bool:
        return self.id < 0

    def _build_non_anki_note_html(self) -> str:
        """
        User's notes should be displayed in a way to visually distinguish between title, text and source.
        Also, text might need to be cut if is too long to reduce time needed for highlighting, extracting keywords, and rendering.
        """
        src     = self.source
        title   = html.escape(self.title)
        body    = self.text


        # old notes where saved with html tags
        # new ones are saved with markdown
        # so the markdown -> html conversion should only be called if the text is not already html
        # markdown conversion should also not be called for meta notes
        if not self.is_meta_note() and not utility.text.is_html(body):
            body    = markdown(body[:3000],extensions=[FencedCodeExtension(), DefListExtension()])


        #trim very long texts:
        # id > 0 because meta cards should not be trimmed
        if len(body) > 2000 and not self.is_meta_note():
            #there might be unclosed tags now, but parsing would be too much overhead, so simply remove div, a and span tags
            #there might be still problems with <p style='...'>
            body                = body[:2000]
            body                = utility.text.remove_tags(body, ["div", "span", "a"])
            last_open_bracket   = body.rfind("<")

            if last_open_bracket >= len(body) - 500 or body.rfind(" ") < len(body) - 500:
                last_close_bracket = body.rfind(">")
                if last_close_bracket < last_open_bracket:
                    body = body[:last_open_bracket]

            body += "<br></ul></b></i></em></span></p></a></p><p class='ta_center' style='user-select: none;'><b>(Text was cut - too long to display)</b></p>"

        # yt vids are prepended with thumbnail image
        if self.is_yt():
            time = utility.text.get_yt_time_verbose(self.source)
            if len(body.strip()) > 0:
                body += "<br/><hr class='siac-note-hr'>"
            body = f"""{body}<p class='flex-row' style='margin: 0;'>
                        <img src='http://img.youtube.com/vi/{utility.text.get_yt_video_id(src)}/0.jpg' style='height: 70px; margin-right: 40px;'/>
                        <span class='flex-col' style='justify-content: center;'>
                            <span class='siac-caps' style='font-size: 13px;'>Saved At
                            <br>
                            <span style='font-size: 25px; line-height: 1em;'>{time}</span>
                            </span>
                        </span>
                        </p>
                    """

        # title   = "%s<b>%s</b>%s" % ("<i class='fa fa-file-pdf-o' style='margin-right: 7px;'></i>" if self.is_pdf() else "", title if len(title) > 0 else "Unnamed Note", "<hr class='mb-5 siac-note-hr'>" if len(body.strip()) > 0 else "")

        # add the source, separated by a line
        if src is not None and len(src) > 0 and get_config_value_or_default("notes.showSource", True):
            if "/" in src and src.endswith(".pdf"):
                src = src[src.rindex("/") +1:]
            if self.is_yt():
                src = f"<a href='{src}'>{src}</a>"
            if len(body) > 0:
                src = f"<hr class='siac-note-hr'><i>Source: {src}</i>"
            else:
                src = f"<i>Source: {src}</i>"
        else:
            src = ""

        return body + src

class IndexNote(Printable):

    note_type: str = "index"

    def __init__(self, props: Tuple[Any, ...]):
        self.id     = props[0]
        self.text   = props[1]
        self.tags   = props[2]
        self.did    = props[3]
        self.source = props[4]
        self.rank   = props[5]
        self.mid    = props[6]
        self.refs   = props[7]


    def get_content(self) -> str:
        return self.source

class NoteRelations():
    def __init__(self, related_by_title: List[SiacNote], related_by_tags: List[SiacNote], related_by_folder: List[SiacNote]):
        self.related_by_title   = related_by_title
        self.related_by_tags    = related_by_tags
        self.related_by_folder  = related_by_folder
