import json
from pathlib import Path
from typing import List, Tuple

import streamlit as st
from streamlit_calendar import calendar

from entities import Evenement, Lieu
import utils


def _load_definitions(definitions_file: Path) -> Tuple[List[Lieu], List[Evenement]]:
    with definitions_file.open("r") as f:
        definitions = json.load(f)
    
    lieux = [Lieu(**ldef) for ldef in definitions["lieux"]]
    events = [Evenement.create(**edef) for edef in definitions["evenements"]]
    return lieux, events


def handle_event_click(event_info):
    st.write("Clicked on:", event_info)


def _get_base_calendar_definition():
    calendar_options = {
        "editable": False,
        "selectable": True,
        "allDaySlot": False,
        "headerToolbar": {
            "left": "prev,next",
            "center": "title",
            "right": "",
        },
        "defaultDate": "0001-01-02",
        "validRange": {
            "start": "0001-01-01",
            "end": "0001-01-08"
        },
        "slotMinTime": "10:00:00",
        "slotMaxTime": "23:00:00",
        "initialView": "resourceTimeGridDay",
        "initialDate": "0001-01-03",
        "contentHeight": "auto",
        "selectMirror": True,
        "titleFormat": {
            "day": "numeric"
        }
    }

    calendar_css = """
        .fc-event-past {
            opacity: 0.8;
        }
        .fc-event-time {
            font-style: italic;
        }
        .fc-event-title {
            font-weight: 700;
        }
        .fc-toolbar-title {
            font-size: 2rem;
        }
    """
    return calendar_options, calendar_css


def _compose_day_calendar(events):
    # create list of resources (lieux)
    lieux = {event.lieu for event in events}
    resources = [lieu.to_fullcalendar() for lieu in lieux]

    # create list of events:
    calendar_events = [event.to_fullcalendar() for event in events]

    # fill calendar
    calendar_options, calendar_css = _get_base_calendar_definition()
    calendar_options["resources"] = resources
    return calendar_events, calendar_options, calendar_css


def display_horaire():
    """
    Not great sepration of responsibilities... 
    Assumes at least one event exists as the date range is defined
    based on the objects passed. This basically assumes something
    from the caller.

    Anyway...
    """
    # load events
    definition_file = utils.get_definitions_file()
    _, events = _load_definitions(definition_file)

    calendar_events, calendar_options, calendar_css = _compose_day_calendar(events)
    return calendar(
        events=calendar_events,
        options=calendar_options,
        custom_css=calendar_css,
        callbacks=["eventClick"]
    )

my_calendar = display_horaire()
