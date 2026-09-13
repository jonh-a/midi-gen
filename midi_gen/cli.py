import os
import sys
from uuid import uuid4

import click
import pretty_midi
from pychord import Chord

from .copy import copy_file_to_clipboard
from .util import fill_pattern, length_to_duration


@click.command()
@click.argument('chords', nargs=-1, required=True, type=str, help="list of chord names")
@click.option('-r', 'root_pitch', default=3, type=int, help="root pitch (octave)")
@click.option('-o', 'output_file', type=str, help="path to output file")
@click.option('-c', 'copy', is_flag=True, help="copy to clipboard")
@click.option('-p', 'pattern', default='q', type=str, help="""chord length pattern
              (s=sixteenth note,
              e=eighth note,
              h=half note,
              w=whole note,
              2=two measures,
              3=three measures,
              4=four mesaures)""")
def generate(
    chords: list[str], 
    root_pitch: int, 
    output_file: str,
    copy: bool,
    pattern: str,
):
    if not output_file and not copy:
        print("either output_file or copy must be set.")
        sys.exit(1)

    pattern = fill_pattern(list(pattern), chords)

    chords_with_components = []
    
    for chord in chords:
        try:
            c = Chord(chord)
            chords_with_components.append(c.components_with_pitch(root_pitch=root_pitch))
        except ValueError:
            print("Invalid chord provided.")
            sys.exit(1)

    midi = pretty_midi.PrettyMIDI()
    chord_program = pretty_midi.instrument_name_to_program('Acoustic Grand Piano')
    chord_track = pretty_midi.Instrument(program=chord_program)
    
    start = 0

    for chord, length in zip(chords_with_components, pattern):
        duration = length_to_duration(length)
        for note_with_pitch in chord:
            midi_number = pretty_midi.note_name_to_number(note_with_pitch)
            midi_note = pretty_midi.Note(
                velocity=100,
                pitch=midi_number,
                start=start,
                end=start + duration
            )
            chord_track.notes.append(midi_note)
            print(chord_track.notes)
        start = start + duration
    
    midi.instruments.append(chord_track)

    if not output_file:
        file_name = f"{uuid4()}.mid"
    else:
        file_name = output_file

    midi.write(file_name)

    if copy:
        copy_file_to_clipboard(file_name)

    if not output_file:
        os.remove(file_name)

    sys.exit(0)
