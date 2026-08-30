#!/usr/bin/env python3
"""
Synthesizes the authentic 8-bit Chiptune BGM for Stage 2 (Inside School Campus):
"Quiet Halls, Hidden Traps" (ทางเดินตึกเรียน & กับดักที่ซ่อนอยู่)
- Tempo: 128 BPM
- Key: E Minor / A Dorian
- Vibe: Peaceful, inquisitive academic vibe with stealthy tension and playful suspense
- Multi-channel: Pulse Lead, Echo Harmony, Deep Walking Bass, Crisp Subtle Percussion
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
    def __init__(self, bpm=128, num_bars=8, beats_per_bar=4):
        self.bpm = bpm
        self.num_bars = num_bars
        self.beats_per_bar = beats_per_bar
        self.beat_duration = 60.0 / bpm
        self.total_duration = num_bars * beats_per_bar * self.beat_duration
        self.total_samples = int(self.total_duration * SAMPLE_RATE)
        self.buffer_left = [0.0] * self.total_samples
        self.buffer_right = [0.0] * self.total_samples

    def add_pulse_note(self, note_name, start_beat, duration_beats, duty=0.5, volume=0.25, pan=0.0, vibrato=False, staccato=False):
        if note_name == 'REST' or note_name is None:
            return
        freq = note_to_freq(note_name)
        start_sample = int(start_beat * self.beat_duration * SAMPLE_RATE)
        play_duration = duration_beats * (0.6 if staccato else 0.95)
        dur_samples = int(play_duration * self.beat_duration * SAMPLE_RATE)
        
        phase = 0.0
        for i in range(dur_samples):
            idx = (start_sample + i) % self.total_samples
            t = i / SAMPLE_RATE
            
            env = min(1.0, i / (SAMPLE_RATE * 0.006))
            rel_len = int(dur_samples * 0.2)
            if i > dur_samples - rel_len:
                env *= (dur_samples - i) / rel_len
                
            cur_freq = freq
            if vibrato and t > 0.15:
                cur_freq += math.sin((t - 0.15) * 28.0) * (freq * 0.015)
                
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
        dur_samples = int(duration_beats * 0.95 * self.beat_duration * SAMPLE_RATE)
        
        phase = 0.0
        for i in range(dur_samples):
            idx = (start_sample + i) % self.total_samples
            env = min(1.0, i / (SAMPLE_RATE * 0.006))
            if i > dur_samples - int(dur_samples * 0.15):
                env *= (dur_samples - i) / int(dur_samples * 0.15)
                
            val = triangle_wave(phase) * volume * env
            phase += freq / SAMPLE_RATE
            self.buffer_left[idx] += val * 0.7
            self.buffer_right[idx] += val * 0.7

    def add_noise_hit(self, hit_type, start_beat, volume=0.18):
        start_sample = int(start_beat * self.beat_duration * SAMPLE_RATE)
        if hit_type == 'kick':
            dur_samples = int(SAMPLE_RATE * 0.07)
            phase = 0.0
            for i in range(dur_samples):
                idx = (start_sample + i) % self.total_samples
                t = i / dur_samples
                f = 110.0 * (1.0 - t) + 32.0
                env = (1.0 - t) ** 2.2
                val = triangle_wave(phase) * volume * 1.3 * env
                phase += f / SAMPLE_RATE
                self.buffer_left[idx] += val
                self.buffer_right[idx] += val
        elif hit_type == 'snare':
            dur_samples = int(SAMPLE_RATE * 0.09)
            noise_val = 0.0
            for i in range(dur_samples):
                idx = (start_sample + i) % self.total_samples
                t = i / dur_samples
                env = (1.0 - t) ** 1.8
                if random.random() < 0.28:
                    noise_val = (random.random() * 2.0 - 1.0)
                val = noise_val * volume * env
                self.buffer_left[idx] += val * 0.85
                self.buffer_right[idx] += val * 0.85
        elif hit_type == 'hat':
            dur_samples = int(SAMPLE_RATE * 0.03)
            for i in range(dur_samples):
                idx = (start_sample + i) % self.total_samples
                t = i / dur_samples
                env = (1.0 - t) ** 3
                val = (random.random() * 2.0 - 1.0) * (volume * 0.45) * env
                self.buffer_left[idx] += val * 0.7
                self.buffer_right[idx] += val * 0.7

    def export_wav(self, filepath):
        max_val = 0.0001
        for i in range(self.total_samples):
            max_val = max(max_val, abs(self.buffer_left[i]), abs(self.buffer_right[i]))
            
        gain = 0.85 / max_val
        
        with open(filepath, 'wb') as f:
            f.write(b'RIFF')
            file_size = 36 + self.total_samples * 4
            f.write(struct.pack('<I', file_size))
            f.write(b'WAVE')
            f.write(b'fmt ')
            f.write(struct.pack('<IHHIIHH', 16, 1, 2, SAMPLE_RATE, SAMPLE_RATE * 4, 4, 16))
            f.write(b'data')
            f.write(struct.pack('<I', self.total_samples * 4))
            
            for i in range(self.total_samples):
                s_l = math.tanh(self.buffer_left[i] * gain)
                s_r = math.tanh(self.buffer_right[i] * gain)
                int_l = max(-32767, min(32767, int(s_l * 32767.0)))
                int_r = max(-32767, min(32767, int(s_r * 32767.0)))
                f.write(struct.pack('<hh', int_l, int_r))

def build_stage2_track(filepath):
    synth = ChiptuneSynth(bpm=128, num_bars=8)

    # 1. Subtle, Inquisitive Percussion (Crisp 8-bit beat)
    for bar in range(8):
        b = bar * 4
        # Kick on 1 and subtle kick on 2.5
        synth.add_noise_hit('kick', b + 0.0, volume=0.22)
        synth.add_noise_hit('hat', b + 0.5, volume=0.15)
        synth.add_noise_hit('snare', b + 1.0, volume=0.16)
        synth.add_noise_hit('hat', b + 1.5, volume=0.15)
        synth.add_noise_hit('kick', b + 2.5, volume=0.18)
        synth.add_noise_hit('snare', b + 3.0, volume=0.16)
        synth.add_noise_hit('hat', b + 3.5, volume=0.15)

    # 2. Stealthy, Groovy Walking Bass (Triangle Wave in Em / Am / C / B7)
    bass_notes = [
        # Bar 1 (Em - Quiet corridor)
        ('E2', 0.0, 0.4), ('E3', 0.5, 0.3), ('G2', 1.0, 0.4), ('B2', 1.5, 0.4),
        ('E2', 2.0, 0.4), ('B2', 2.5, 0.3), ('D3', 3.0, 0.4), ('D#3', 3.5, 0.3),
        # Bar 2 (Em - Tense footsteps)
        ('E2', 4.0, 0.4), ('E3', 4.5, 0.3), ('G2', 5.0, 0.4), ('A2', 5.5, 0.4),
        ('A#2', 6.0, 0.4), ('B2', 6.5, 0.4), ('D3', 7.0, 0.4), ('B2', 7.5, 0.3),
        # Bar 3 (Am - Classroom shadows)
        ('A2', 8.0, 0.4), ('A3', 8.5, 0.3), ('C3', 9.0, 0.4), ('E3', 9.5, 0.4),
        ('A2', 10.0, 0.4), ('E3', 10.5, 0.3), ('G3', 11.0, 0.4), ('E3', 11.5, 0.3),
        # Bar 4 (B7 - Suspense / Teacher around corner)
        ('B2', 12.0, 0.4), ('D#3', 12.5, 0.4), ('F#3', 13.0, 0.4), ('A3', 13.5, 0.4),
        ('B2', 14.0, 0.4), ('F#3', 14.5, 0.3), ('G3', 15.0, 0.3), ('F#3', 15.5, 0.3),
        # Bar 5 (C -> D - Sneaking upstairs)
        ('C3', 16.0, 0.4), ('E3', 16.5, 0.3), ('G3', 17.0, 0.4), ('C4', 17.5, 0.4),
        ('D3', 18.0, 0.4), ('F#3', 18.5, 0.3), ('A3', 19.0, 0.4), ('D4', 19.5, 0.4),
        # Bar 6 (Em -> D)
        ('E3', 20.0, 0.4), ('B2', 20.5, 0.3), ('G2', 21.0, 0.4), ('E2', 21.5, 0.4),
        ('D3', 22.0, 0.4), ('A2', 22.5, 0.3), ('F#2', 23.0, 0.4), ('D2', 23.5, 0.4),
        # Bar 7 (C -> B7)
        ('C3', 24.0, 0.4), ('G2', 24.5, 0.3), ('E2', 25.0, 0.4), ('C2', 25.5, 0.4),
        ('B2', 26.0, 0.4), ('D#3', 26.5, 0.4), ('F#3', 27.0, 0.4), ('A3', 27.5, 0.4),
        # Bar 8 (Em resolve)
        ('E2', 28.0, 0.6), ('B2', 29.0, 0.4), ('E3', 29.5, 0.4),
        ('G3', 30.0, 0.3), ('F#3', 30.5, 0.3), ('D#3', 31.0, 0.3), ('D3', 31.5, 0.3)
    ]
    for n, s, d in bass_notes:
        synth.add_triangle_note(n, s, d, volume=0.32)

    # 3. Main Melody: "School Stealth & Tension" (Pulse 50% - Playful, sneaky, melodious)
    lead_notes = [
        # Bar 1: Sneaky staccato intro
        ('B4', 0.0, 0.35, True), ('E5', 0.5, 0.35, True), ('G5', 1.0, 0.4, False),
        ('F#5', 1.75, 0.4, False), ('E5', 2.25, 0.6, True), ('D#5', 3.0, 0.4, False), ('E5', 3.5, 0.4, False),
        # Bar 2: Inquisitive question
        ('B4', 4.0, 0.35, True), ('D5', 4.5, 0.35, True), ('E5', 5.0, 0.8, False),
        ('G5', 6.0, 0.35, True), ('A5', 6.5, 0.35, True), ('B5', 7.0, 0.8, True),
        # Bar 3: Mysterious classroom theme
        ('C6', 8.0, 0.5, False), ('B5', 8.75, 0.4, False), ('A5', 9.5, 0.6, False),
        ('E5', 10.5, 0.4, False), ('G5', 11.0, 0.4, False), ('A5', 11.5, 0.4, False),
        # Bar 4: Suspenseful teacher alert!
        ('B5', 12.0, 0.5, False), ('A5', 12.75, 0.4, False), ('F#5', 13.5, 0.6, False),
        ('D#5', 14.5, 0.4, False), ('F#5', 15.0, 0.4, False), ('A5', 15.5, 0.4, False),
        # Bar 5: Upbeat courage - Dash through hallway!
        ('G5', 16.0, 0.4, False), ('A5', 16.5, 0.4, False), ('B5', 17.0, 0.8, False),
        ('A5', 18.0, 0.4, False), ('B5', 18.5, 0.4, False), ('C6', 19.0, 0.8, False),
        # Bar 6: Heroic stair climb
        ('B5', 20.0, 0.5, False), ('G5', 20.75, 0.4, False), ('E5', 21.5, 0.8, False),
        ('D5', 22.5, 0.4, False), ('E5', 23.0, 0.4, False), ('F#5', 23.5, 0.4, False),
        # Bar 7: Dramatic climax
        ('G5', 24.0, 0.5, False), ('E5', 24.75, 0.4, False), ('C5', 25.5, 0.6, False),
        ('F#5', 26.5, 0.4, False), ('D#5', 27.0, 0.4, False), ('B4', 27.5, 0.6, False),
        # Bar 8: Resolve to calm
        ('E5', 28.0, 1.2, True), ('G5', 29.5, 0.4, False), ('F#5', 30.0, 0.4, False),
        ('D#5', 30.5, 0.4, False), ('E5', 31.0, 0.8, True)
    ]
    for note_info in lead_notes:
        n, s, d, stac = note_info
        synth.add_pulse_note(n, s, d, duty=0.5, volume=0.26, pan=-0.15, vibrato=True, staccato=stac)

    # 4. Echo Harmony & Subtle Bells (Pulse 25% - Creates the school atmosphere)
    echo_notes = [
        # Off-beat harmonious accents
        ('G4', 0.25, 0.2), ('B4', 0.75, 0.2), ('E5', 1.25, 0.2), ('G4', 2.25, 0.2),
        ('G4', 4.25, 0.2), ('B4', 4.75, 0.2), ('E5', 5.25, 0.2), ('E5', 7.25, 0.2),
        ('E4', 8.25, 0.2), ('A4', 8.75, 0.2), ('C5', 9.25, 0.2), ('E4', 10.25, 0.2),
        ('D#4', 12.25, 0.2), ('F#4', 12.75, 0.2), ('A4', 13.25, 0.2), ('B4', 14.25, 0.2),
        ('E4', 16.25, 0.2), ('G4', 16.75, 0.2), ('B4', 17.25, 0.2), ('C5', 19.25, 0.2),
        ('G4', 20.25, 0.2), ('B4', 20.75, 0.2), ('E5', 21.25, 0.2), ('D5', 22.25, 0.2),
        ('E4', 24.25, 0.2), ('G4', 24.75, 0.2), ('A4', 25.25, 0.2), ('B4', 26.25, 0.2),
        ('B4', 28.25, 0.4), ('G4', 29.25, 0.3), ('E4', 30.25, 0.3), ('E4', 31.25, 0.3)
    ]
    for n, s, d in echo_notes:
        synth.add_pulse_note(n, s, d, duty=0.25, volume=0.12, pan=0.25, vibrato=False, staccato=True)

    synth.export_wav(filepath)

if __name__ == '__main__':
    audio_dir = r'Assets/Audio'
    res_dir = r'Assets/Resources/Audio'
    os.makedirs(audio_dir, exist_ok=True)
    os.makedirs(res_dir, exist_ok=True)

    t_path1 = os.path.join(audio_dir, 'bgm_stage2_school_corridor.wav')
    t_path2 = os.path.join(res_dir, 'bgm_stage2_school_corridor.wav')

    print('Synthesizing Stage 2 BGM: "Quiet Halls, Hidden Traps"...')
    build_stage2_track(t_path1)
    build_stage2_track(t_path2)

    # Generate meta files
    template = '''fileFormatVersion: 2
guid: {guid}
AudioImporter:
  serializedVersion: 6
  defaultSettings:
    loadType: 0
    sampleRateSetting: 0
    sampleRateOverride: 44100
    compressionFormat: 0
    quality: 1
    conversionMode: 0
  customSettings: {{}}
  forceToMono: 0
  normalize: 1
  preloadAudioData: 1
  loadInBackground: 0
  ambisonic: 0
  3D: 0
  userData: 
  assetBundleName: 
  assetBundleVariant: 
'''
    g1 = uuid.uuid5(uuid.NAMESPACE_DNS, 'audio_bgm_stage2_school_corridor.wav').hex
    g2 = uuid.uuid5(uuid.NAMESPACE_DNS, 'res_audio_bgm_stage2_school_corridor.wav').hex
    with open(t_path1 + '.meta', 'w', encoding='utf-8') as f:
        f.write(template.format(guid=g1))
    with open(t_path2 + '.meta', 'w', encoding='utf-8') as f:
        f.write(template.format(guid=g2))

    print('Stage 2 BGM synthesized and meta files created successfully!')
