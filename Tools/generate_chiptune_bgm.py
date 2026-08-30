#!/usr/bin/env python3
"""
Synthesizes 3 authentic 8-bit Chiptune BGM loop tracks for Stage 1 (Dorm to Campus Rush).
Uses multi-channel NES/GameBoy sound emulation:
- 2 Pulse/Square Wave Channels (Lead Melody + Harmony Arpeggio)
- 1 Triangle Wave Channel (Punchy 8-bit Bassline)
- 1 Pseudo-Random Noise Channel (8-bit Snare, Kick & Hi-hats)
Outputs 44.1kHz 16-bit Stereo WAV files.
"""

import os
import math
import struct
import random
import uuid

SAMPLE_RATE = 44100

def note_to_freq(note_name):
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    name = note_name[:-1]
    octave = int(note_name[-1])
    semitone = notes.index(name)
    # A4 = 440Hz, midi note 69
    midi = (octave + 1) * 12 + semitone
    return 440.0 * (2.0 ** ((midi - 69) / 12.0))

def pulse_wave(phase, duty=0.5):
    p = phase % 1.0
    return 1.0 if p < duty else -1.0

def triangle_wave(phase):
    p = phase % 1.0
    if p < 0.5:
        return 4.0 * p - 1.0
    else:
        return 3.0 - 4.0 * p

class ChiptuneSynth:
    def __init__(self, bpm=150, num_bars=8, beats_per_bar=4):
        self.bpm = bpm
        self.num_bars = num_bars
        self.beats_per_bar = beats_per_bar
        self.beat_duration = 60.0 / bpm
        self.total_duration = num_bars * beats_per_bar * self.beat_duration
        self.total_samples = int(self.total_duration * SAMPLE_RATE)
        self.buffer_left = [0.0] * self.total_samples
        self.buffer_right = [0.0] * self.total_samples

    def add_pulse_note(self, note_name, start_beat, duration_beats, duty=0.5, volume=0.25, pan=0.0, vibrato=False):
        if note_name == 'REST' or note_name is None:
            return
        freq = note_to_freq(note_name)
        start_sample = int(start_beat * self.beat_duration * SAMPLE_RATE)
        dur_samples = int(duration_beats * self.beat_duration * SAMPLE_RATE)
        
        phase = 0.0
        for i in range(dur_samples):
            idx = (start_sample + i) % self.total_samples
            t = i / SAMPLE_RATE
            
            # Simple envelope (attack + decay)
            env = min(1.0, i / (SAMPLE_RATE * 0.008)) # Fast attack
            # Release towards end of note
            rel_len = int(dur_samples * 0.15)
            if i > dur_samples - rel_len:
                env *= (dur_samples - i) / rel_len
                
            cur_freq = freq
            if vibrato and t > 0.1:
                cur_freq += math.sin((t - 0.1) * 35.0) * (freq * 0.02)
                
            val = pulse_wave(phase, duty) * volume * env
            phase += cur_freq / SAMPLE_RATE
            
            vol_l = (1.0 - pan) * 0.5 + 0.5
            vol_r = (1.0 + pan) * 0.5 + 0.5
            self.buffer_left[idx] += val * vol_l
            self.buffer_right[idx] += val * vol_r

    def add_triangle_note(self, note_name, start_beat, duration_beats, volume=0.35):
        if note_name == 'REST' or note_name is None:
            return
        freq = note_to_freq(note_name)
        start_sample = int(start_beat * self.beat_duration * SAMPLE_RATE)
        dur_samples = int(duration_beats * self.beat_duration * SAMPLE_RATE)
        
        phase = 0.0
        for i in range(dur_samples):
            idx = (start_sample + i) % self.total_samples
            env = min(1.0, i / (SAMPLE_RATE * 0.005))
            if i > dur_samples - int(dur_samples * 0.1):
                env *= (dur_samples - i) / int(dur_samples * 0.1)
                
            val = triangle_wave(phase) * volume * env
            phase += freq / SAMPLE_RATE
            self.buffer_left[idx] += val * 0.7
            self.buffer_right[idx] += val * 0.7

    def add_noise_hit(self, hit_type, start_beat, volume=0.2):
        start_sample = int(start_beat * self.beat_duration * SAMPLE_RATE)
        if hit_type == 'kick':
            dur_samples = int(SAMPLE_RATE * 0.08)
            phase = 0.0
            for i in range(dur_samples):
                idx = (start_sample + i) % self.total_samples
                t = i / dur_samples
                f = 120.0 * (1.0 - t) + 35.0
                env = (1.0 - t) ** 2
                val = triangle_wave(phase) * volume * 1.5 * env
                phase += f / SAMPLE_RATE
                self.buffer_left[idx] += val
                self.buffer_right[idx] += val
        elif hit_type == 'snare':
            dur_samples = int(SAMPLE_RATE * 0.12)
            noise_val = 0.0
            for i in range(dur_samples):
                idx = (start_sample + i) % self.total_samples
                t = i / dur_samples
                env = (1.0 - t) ** 1.5
                if random.random() < 0.3:
                    noise_val = (random.random() * 2.0 - 1.0)
                val = noise_val * volume * env
                self.buffer_left[idx] += val * 0.9
                self.buffer_right[idx] += val * 0.9
        elif hit_type == 'hat':
            dur_samples = int(SAMPLE_RATE * 0.04)
            for i in range(dur_samples):
                idx = (start_sample + i) % self.total_samples
                t = i / dur_samples
                env = (1.0 - t) ** 3
                val = (random.random() * 2.0 - 1.0) * (volume * 0.6) * env
                self.buffer_left[idx] += val * 0.8
                self.buffer_right[idx] += val * 0.8

    def export_wav(self, filepath):
        # Master volume normalization and soft clipping
        max_val = 0.0001
        for i in range(self.total_samples):
            max_val = max(max_val, abs(self.buffer_left[i]), abs(self.buffer_right[i]))
            
        gain = 0.85 / max_val
        
        with open(filepath, 'wb') as f:
            # WAV Header
            f.write(b'RIFF')
            file_size = 36 + self.total_samples * 4
            f.write(struct.pack('<I', file_size))
            f.write(b'WAVE')
            f.write(b'fmt ')
            f.write(struct.pack('<IHHIIHH', 16, 1, 2, SAMPLE_RATE, SAMPLE_RATE * 4, 4, 16))
            f.write(b'data')
            f.write(struct.pack('<I', self.total_samples * 4))
            
            for i in range(self.total_samples):
                # Soft tanh limiting
                s_l = math.tanh(self.buffer_left[i] * gain)
                s_r = math.tanh(self.buffer_right[i] * gain)
                int_l = max(-32767, min(32767, int(s_l * 32767.0)))
                int_r = max(-32767, min(32767, int(s_r * 32767.0)))
                f.write(struct.pack('<hh', int_l, int_r))

# -------------------------------------------------------------
# TRACK 1: "Morning Panic! 8:25 AM" (สายแล้วโว้ยยย!)
# Fast, bouncy, frantic comedy rush (156 BPM)
# -------------------------------------------------------------
def build_track1(filepath):
    synth = ChiptuneSynth(bpm=156, num_bars=8)
    
    # Drums
    for bar in range(8):
        b = bar * 4
        synth.add_noise_hit('kick', b + 0.0)
        synth.add_noise_hit('hat', b + 0.5)
        synth.add_noise_hit('snare', b + 1.0)
        synth.add_noise_hit('hat', b + 1.5)
        synth.add_noise_hit('kick', b + 2.0)
        synth.add_noise_hit('hat', b + 2.5)
        synth.add_noise_hit('snare', b + 3.0)
        synth.add_noise_hit('hat', b + 3.5)

    # Bassline (Bouncy Walking Triangle Bass)
    bass_notes = [
        # Bar 1 (C)
        ('C3', 0.0, 0.4), ('C3', 0.5, 0.4), ('E3', 1.0, 0.4), ('G3', 1.5, 0.4),
        ('C3', 2.0, 0.4), ('G3', 2.5, 0.4), ('A3', 3.0, 0.4), ('B3', 3.5, 0.4),
        # Bar 2 (Am)
        ('A2', 4.0, 0.4), ('A2', 4.5, 0.4), ('C3', 5.0, 0.4), ('E3', 5.5, 0.4),
        ('A2', 6.0, 0.4), ('E3', 6.5, 0.4), ('F3', 7.0, 0.4), ('G3', 7.5, 0.4),
        # Bar 3 (F)
        ('F2', 8.0, 0.4), ('F2', 8.5, 0.4), ('A2', 9.0, 0.4), ('C3', 9.5, 0.4),
        ('F2', 10.0, 0.4), ('C3', 10.5, 0.4), ('D3', 11.0, 0.4), ('D#3', 11.5, 0.4),
        # Bar 4 (G)
        ('G2', 12.0, 0.4), ('G2', 12.5, 0.4), ('B2', 13.0, 0.4), ('D3', 13.5, 0.4),
        ('G2', 14.0, 0.4), ('D3', 14.5, 0.4), ('G3', 15.0, 0.4), ('F3', 15.5, 0.4),
        # Bar 5 (C)
        ('C3', 16.0, 0.4), ('C3', 16.5, 0.4), ('E3', 17.0, 0.4), ('G3', 17.5, 0.4),
        ('C3', 18.0, 0.4), ('G3', 18.5, 0.4), ('E3', 19.0, 0.4), ('C3', 19.5, 0.4),
        # Bar 6 (Am)
        ('A2', 20.0, 0.4), ('A2', 20.5, 0.4), ('C3', 21.0, 0.4), ('E3', 21.5, 0.4),
        ('A2', 22.0, 0.4), ('E3', 22.5, 0.4), ('C3', 23.0, 0.4), ('A2', 23.5, 0.4),
        # Bar 7 (F -> G)
        ('F2', 24.0, 0.4), ('A2', 24.5, 0.4), ('C3', 25.0, 0.4), ('F3', 25.5, 0.4),
        ('G2', 26.0, 0.4), ('B2', 26.5, 0.4), ('D3', 27.0, 0.4), ('G3', 27.5, 0.4),
        # Bar 8 (C turnaround)
        ('C3', 28.0, 0.4), ('G2', 28.5, 0.4), ('E2', 29.0, 0.4), ('C2', 29.5, 0.4),
        ('G2', 30.0, 0.3), ('A2', 30.5, 0.3), ('B2', 31.0, 0.3), ('B2', 31.5, 0.3)
    ]
    for n, s, d in bass_notes:
        synth.add_triangle_note(n, s, d)

    # Lead Melody (Square 50% - Frantic & Catchy)
    lead_notes = [
        # Bar 1
        ('E5', 0.0, 0.4), ('E5', 0.5, 0.4), ('E5', 1.0, 0.4), ('C5', 1.5, 0.4),
        ('E5', 2.0, 0.4), ('G5', 2.5, 0.9), ('G4', 3.5, 0.4),
        # Bar 2
        ('C5', 4.0, 0.6), ('G4', 4.75, 0.4), ('E4', 5.25, 0.6),
        ('A4', 6.0, 0.4), ('B4', 6.5, 0.4), ('A#4', 7.0, 0.4), ('A4', 7.5, 0.4),
        # Bar 3
        ('G4', 8.0, 0.4), ('E5', 8.5, 0.4), ('G5', 9.0, 0.4), ('A5', 9.5, 0.8),
        ('F5', 10.5, 0.4), ('G5', 11.0, 0.4), ('E5', 11.5, 0.4),
        # Bar 4
        ('C5', 12.0, 0.4), ('D5', 12.5, 0.4), ('B4', 13.0, 0.8),
        ('G4', 14.0, 0.4), ('A4', 14.5, 0.4), ('B4', 15.0, 0.4), ('D5', 15.5, 0.4),
        # Bar 5
        ('E5', 16.0, 0.4), ('G5', 16.5, 0.4), ('C6', 17.0, 0.8),
        ('B5', 18.0, 0.4), ('A5', 18.5, 0.4), ('G5', 19.0, 0.8),
        # Bar 6
        ('E5', 20.0, 0.4), ('C5', 20.5, 0.4), ('A4', 21.0, 0.8),
        ('F5', 22.0, 0.4), ('E5', 22.5, 0.4), ('D5', 23.0, 0.8),
        # Bar 7
        ('C5', 24.0, 0.4), ('D5', 24.5, 0.4), ('E5', 25.0, 0.4), ('F5', 25.5, 0.4),
        ('G5', 26.0, 0.4), ('A5', 26.5, 0.4), ('B5', 27.0, 0.8),
        # Bar 8
        ('C6', 28.0, 1.0), ('G5', 29.25, 0.5), ('E5', 29.75, 0.5),
        ('D5', 30.5, 0.4), ('D#5', 31.0, 0.4), ('E5', 31.5, 0.4)
    ]
    for n, s, d in lead_notes:
        synth.add_pulse_note(n, s, d, duty=0.5, volume=0.28, pan=-0.2, vibrato=True)

    # Arpeggio Chords (Pulse 25% - High sparkle)
    arp_chords = [
        (['C5', 'E5', 'G5', 'C6'], 0, 4),
        (['A4', 'C5', 'E5', 'A5'], 4, 8),
        (['F4', 'A4', 'C5', 'F5'], 8, 12),
        (['G4', 'B4', 'D5', 'G5'], 12, 16),
        (['C5', 'E5', 'G5', 'C6'], 16, 20),
        (['A4', 'C5', 'E5', 'A5'], 20, 24),
        (['F4', 'A4', 'C5', 'F5'], 24, 28),
        (['G4', 'B4', 'D5', 'G5'], 28, 32),
    ]
    for chord, s_beat, e_beat in arp_chords:
        for b in range(int((e_beat - s_beat) * 4)):
            t_beat = s_beat + b * 0.25
            n = chord[b % len(chord)]
            synth.add_pulse_note(n, t_beat, 0.2, duty=0.25, volume=0.12, pan=0.3)

    synth.export_wav(filepath)

# -------------------------------------------------------------
# TRACK 2: "Chalong Krung Sprint" (สับตีนแตก ถนนฉลองกรุง)
# Driving 8-bit Synth-Funk & Street Rush (144 BPM)
# -------------------------------------------------------------
def build_track2(filepath):
    synth = ChiptuneSynth(bpm=144, num_bars=8)
    
    # Driving Funk Beat
    for bar in range(8):
        b = bar * 4
        synth.add_noise_hit('kick', b + 0.0)
        synth.add_noise_hit('hat', b + 0.5)
        synth.add_noise_hit('snare', b + 1.0)
        synth.add_noise_hit('hat', b + 1.5)
        synth.add_noise_hit('kick', b + 1.75)
        synth.add_noise_hit('kick', b + 2.25)
        synth.add_noise_hit('snare', b + 3.0)
        synth.add_noise_hit('hat', b + 3.5)

    # Slap-style Triangle Bassline
    bass_notes = [
        # Dm Groove
        ('D2', 0.0, 0.3), ('D3', 0.5, 0.2), ('D2', 1.0, 0.3), ('F2', 1.5, 0.3),
        ('G2', 2.0, 0.3), ('G#2', 2.5, 0.2), ('A2', 3.0, 0.3), ('C3', 3.5, 0.3),
        ('D2', 4.0, 0.3), ('D3', 4.5, 0.2), ('D2', 5.0, 0.3), ('F2', 5.5, 0.3),
        ('C3', 6.0, 0.3), ('A2', 6.5, 0.3), ('G2', 7.0, 0.3), ('F2', 7.5, 0.3),
        # Bb -> C
        ('A#2', 8.0, 0.3), ('A#3', 8.5, 0.2), ('A#2', 9.0, 0.3), ('D3', 9.5, 0.3),
        ('C3', 10.0, 0.3), ('C4', 10.5, 0.2), ('C3', 11.0, 0.3), ('E3', 11.5, 0.3),
        # Dm
        ('D2', 12.0, 0.3), ('D3', 12.5, 0.2), ('F2', 13.0, 0.3), ('G2', 13.5, 0.3),
        ('A2', 14.0, 0.3), ('C3', 14.5, 0.3), ('D3', 15.0, 0.4), ('D2', 15.5, 0.3),
        # Second half
        ('D2', 16.0, 0.3), ('D3', 16.5, 0.2), ('D2', 17.0, 0.3), ('F2', 17.5, 0.3),
        ('G2', 18.0, 0.3), ('G#2', 18.5, 0.2), ('A2', 19.0, 0.3), ('C3', 19.5, 0.3),
        ('D2', 20.0, 0.3), ('D3', 20.5, 0.2), ('D2', 21.0, 0.3), ('F2', 21.5, 0.3),
        ('C3', 22.0, 0.3), ('A2', 22.5, 0.3), ('G2', 23.0, 0.3), ('F2', 23.5, 0.3),
        # Gm -> A7
        ('G2', 24.0, 0.3), ('A#2', 24.5, 0.3), ('D3', 25.0, 0.3), ('G3', 25.5, 0.3),
        ('A2', 26.0, 0.3), ('C#3', 26.5, 0.3), ('E3', 27.0, 0.3), ('A3', 27.5, 0.3),
        ('D2', 28.0, 0.4), ('A2', 28.5, 0.4), ('D3', 29.0, 0.4), ('F3', 29.5, 0.4),
        ('A3', 30.0, 0.3), ('G3', 30.5, 0.3), ('F3', 31.0, 0.3), ('E3', 31.5, 0.3),
    ]
    for n, s, d in bass_notes:
        synth.add_triangle_note(n, s, d)

    # Funky Lead Melody
    lead_notes = [
        ('D5', 0.0, 0.5), ('F5', 0.75, 0.5), ('G5', 1.5, 0.4), ('G#5', 2.0, 0.4),
        ('A5', 2.5, 0.8), ('D5', 3.5, 0.4),
        ('C5', 4.0, 0.4), ('D5', 4.5, 0.8), ('F5', 5.5, 0.4), ('D5', 6.0, 0.8),
        ('A4', 7.0, 0.4), ('C5', 7.5, 0.4),
        ('D5', 8.0, 0.5), ('F5', 8.75, 0.5), ('G5', 9.5, 0.4), ('A5', 10.0, 0.8),
        ('C6', 11.0, 0.4), ('A5', 11.5, 0.8),
        ('G5', 12.5, 0.4), ('F5', 13.0, 0.4), ('D5', 13.5, 0.8),
        ('F5', 14.5, 0.4), ('E5', 15.0, 0.4), ('D5', 15.5, 0.4),
        # High Solo Part
        ('D5', 16.0, 0.4), ('D5', 16.5, 0.4), ('F5', 17.0, 0.4), ('A5', 17.5, 0.4),
        ('D6', 18.0, 0.8), ('C6', 19.0, 0.4), ('A5', 19.5, 0.8),
        ('G5', 20.5, 0.4), ('A5', 21.0, 0.4), ('F5', 21.5, 0.8),
        ('D5', 22.5, 0.4), ('C5', 23.0, 0.4), ('D5', 23.5, 0.4),
        ('G5', 24.0, 0.5), ('A#5', 24.75, 0.5), ('D6', 25.5, 0.8),
        ('C#6', 26.5, 0.5), ('E6', 27.25, 0.6),
        ('D6', 28.0, 1.2), ('A5', 29.5, 0.4), ('F5', 30.0, 0.4), ('E5', 30.5, 0.4), ('D5', 31.0, 0.8)
    ]
    for n, s, d in lead_notes:
        synth.add_pulse_note(n, s, d, duty=0.5, volume=0.27, pan=0.15, vibrato=True)

    synth.export_wav(filepath)

# -------------------------------------------------------------
# TRACK 3: "Campus Dash 8-Bit Hero" (ภารกิจวิ่งสู้ฟัด)
# Heroic, Melodic Japanese Retro Action Platformer (140 BPM)
# -------------------------------------------------------------
def build_track3(filepath):
    synth = ChiptuneSynth(bpm=140, num_bars=8)
    
    # Upbeat Rock Chiptune Beat
    for bar in range(8):
        b = bar * 4
        synth.add_noise_hit('kick', b + 0.0)
        synth.add_noise_hit('hat', b + 0.5)
        synth.add_noise_hit('snare', b + 1.0)
        synth.add_noise_hit('hat', b + 1.5)
        synth.add_noise_hit('kick', b + 2.0)
        synth.add_noise_hit('hat', b + 2.5)
        synth.add_noise_hit('snare', b + 3.0)
        synth.add_noise_hit('hat', b + 3.5)

    # Driving Melodic Bass
    bass_notes = [
        # G
        ('G2', 0.0, 0.4), ('G2', 0.5, 0.4), ('B2', 1.0, 0.4), ('D3', 1.5, 0.4),
        ('G2', 2.0, 0.4), ('D3', 2.5, 0.4), ('G3', 3.0, 0.4), ('F#3', 3.5, 0.4),
        # Em
        ('E2', 4.0, 0.4), ('E2', 4.5, 0.4), ('G2', 5.0, 0.4), ('B2', 5.5, 0.4),
        ('E2', 6.0, 0.4), ('B2', 6.5, 0.4), ('E3', 7.0, 0.4), ('D3', 7.5, 0.4),
        # C
        ('C2', 8.0, 0.4), ('C2', 8.5, 0.4), ('E2', 9.0, 0.4), ('G2', 9.5, 0.4),
        ('C3', 10.0, 0.4), ('G2', 10.5, 0.4), ('E2', 11.0, 0.4), ('C2', 11.5, 0.4),
        # D
        ('D2', 12.0, 0.4), ('D2', 12.5, 0.4), ('F#2', 13.0, 0.4), ('A2', 13.5, 0.4),
        ('D3', 14.0, 0.4), ('A2', 14.5, 0.4), ('F#2', 15.0, 0.4), ('D2', 15.5, 0.4),
        # G -> Bm
        ('G2', 16.0, 0.4), ('B2', 16.5, 0.4), ('D3', 17.0, 0.4), ('G3', 17.5, 0.4),
        ('B2', 18.0, 0.4), ('D3', 18.5, 0.4), ('F#3', 19.0, 0.4), ('B3', 19.5, 0.4),
        # C -> D
        ('C3', 20.0, 0.4), ('E3', 20.5, 0.4), ('G3', 21.0, 0.4), ('C4', 21.5, 0.4),
        ('D3', 22.0, 0.4), ('F#3', 22.5, 0.4), ('A3', 23.0, 0.4), ('D4', 23.5, 0.4),
        # G Cadence
        ('G2', 24.0, 0.4), ('D3', 24.5, 0.4), ('G3', 25.0, 0.4), ('B3', 25.5, 0.4),
        ('C3', 26.0, 0.4), ('D3', 27.0, 0.4), ('G2', 28.0, 1.2),
        ('D2', 30.0, 0.4), ('F#2', 30.5, 0.4), ('A2', 31.0, 0.4), ('D3', 31.5, 0.4),
    ]
    for n, s, d in bass_notes:
        synth.add_triangle_note(n, s, d)

    # Heroic Anime / Retro Game Lead Melody
    lead_notes = [
        ('B4', 0.0, 0.4), ('D5', 0.5, 0.4), ('G5', 1.0, 0.8),
        ('F#5', 2.0, 0.4), ('E5', 2.5, 0.4), ('D5', 3.0, 0.8),
        ('E5', 4.0, 0.4), ('G5', 4.5, 0.4), ('B5', 5.0, 0.8),
        ('A5', 6.0, 0.4), ('G5', 6.5, 0.4), ('F#5', 7.0, 0.8),
        ('G5', 8.0, 0.4), ('A5', 8.5, 0.4), ('E5', 9.0, 0.8),
        ('G5', 10.0, 0.4), ('F#5', 10.5, 0.4), ('E5', 11.0, 0.8),
        ('D5', 12.0, 0.4), ('E5', 12.5, 0.4), ('F#5', 13.0, 0.4), ('A5', 13.5, 0.4),
        ('D6', 14.0, 1.0), ('C6', 15.25, 0.4), ('B5', 15.75, 0.4),
        # Heroic climax
        ('B5', 16.0, 0.6), ('A5', 16.75, 0.4), ('G5', 17.25, 0.6),
        ('F#5', 18.0, 0.4), ('G5', 18.5, 0.4), ('A5', 19.0, 0.8),
        ('G5', 20.0, 0.4), ('A5', 20.5, 0.4), ('B5', 21.0, 0.8),
        ('A5', 22.0, 0.4), ('B5', 22.5, 0.4), ('C6', 23.0, 0.8),
        ('D6', 24.0, 0.8), ('B5', 25.0, 0.4), ('G5', 25.5, 0.8),
        ('E5', 26.5, 0.4), ('A5', 27.0, 0.8), ('F#5', 28.0, 0.4),
        ('G5', 28.5, 1.5)
    ]
    for n, s, d in lead_notes:
        synth.add_pulse_note(n, s, d, duty=0.5, volume=0.28, pan=-0.1, vibrato=True)

    synth.export_wav(filepath)

if __name__ == '__main__':
    audio_dir = r'Assets/Audio'
    os.makedirs(audio_dir, exist_ok=True)
    
    t1_path = os.path.join(audio_dir, 'bgm_stage1_morning_panic.wav')
    t2_path = os.path.join(audio_dir, 'bgm_stage1_street_sprint.wav')
    t3_path = os.path.join(audio_dir, 'bgm_stage1_campus_hero.wav')
    
    print('Generating Track 1: Morning Panic! 8:25 AM...')
    build_track1(t1_path)
    print('Generating Track 2: Chalong Krung Sprint...')
    build_track2(t2_path)
    print('Generating Track 3: Campus Dash 8-Bit Hero...')
    build_track3(t3_path)
    
    print('All 3 chiptune tracks successfully synthesized!')
