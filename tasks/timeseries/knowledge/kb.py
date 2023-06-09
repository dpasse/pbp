from requests.structures import CaseInsensitiveDict

kb = CaseInsensitiveDict({
    '1st': 'quarter-1',
    '2nd': 'quarter-2',
    '3rd': 'quarter-3',
    '4th': 'quarter-4',
    'OT': 'quarter-5',
    'touchdown': 'event-1',
    'field goal': 'event-2',
    'safety': 'event-3',
    'penalty': 'event-4',
    'kicks': 'event-5',
    'punts': 'event-6',
    'intercepted': 'event-7',
    'fumbles': 'event-8',
    'sacked': 'event-9',
    'recovered': 'event-10',
    'timeout': 'event-11',
    'no huddle': 'formation-1',
    'shotgun': 'formation-2',
    'shot gun': 'formation-2',
    'pass formation': 'formation-3',
    'punt formation': 'formation-4',
    'run formation': 'formation-5',
    'field goal formation': 'formation-6',
    'kick formation': 'formation-7'
})

reversed_kb_mappings = {
    'quarter-1': '1st Quarter',
    'quarter-2': '2nd Quarter', 
    'quarter-3': '3rd Quarter',
    'quarter-4': '4th Quarter',
    'quarter-5': 'Overtime',
    'event-1': 'TD',
    'event-2': 'FG',
    'event-3': 'SAFETY',
    'event-4': 'PENALTY',
    'event-5': 'KO',
    'event-6': 'PUNT',
    'event-7': 'INT',
    'event-8': 'FUM',
    'event-9': 'SACKED',
    'event-10': 'FR',
    'event-11': 'TO',
    'formation-1': 'NO HUDDLE',
    'formation-2': 'SHOTGUN',
    'formation-3': 'PASS',
    'formation-4': 'PUNT',
    'formation-5': 'RUN',
    'formation-6': 'FG',
    'formation-7': 'KO',
}