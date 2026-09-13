import os
import sys
from uuid import uuid4

import click
import pretty_midi
from pychord import Chord

from .copy import copy_file_to_clipboard


@click.command()
@click.argument('chords', nargs=-1, required=True, type=str)
@click.option('-p', 'root_pitch', default=3, type=int)
@click.option('-o', 'output_file', type=str)
@click.option('-c', 'copy', is_flag=True)
def generate(
    chords: list[str], 
    root_pitch: int, 
    output_file: str,
    copy: bool,
):
    if not output_file and not copy:
        print("Either output_file or copy must be set.")
        sys.exit(1)

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
    
    for n, chord in enumerate(chords_with_components):
        for note_with_pitch in chord:
            length = 1
            midi_number = pretty_midi.note_name_to_number(note_with_pitch)
            midi_note = pretty_midi.Note(
                velocity=100,
                pitch=midi_number,
                start=n * length,
                end=(n + 1) * length
            )
            chord_track.notes.append(midi_note)
    
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
    
    print(chords_with_components)
