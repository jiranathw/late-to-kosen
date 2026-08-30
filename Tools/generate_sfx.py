#!/usr/bin/env python3
"""
Synthesizes 4 authentic 8-bit chiptune sound effects:
1. sfx_jump.wav        - Classic retro rising pitch slide (0.12s)
2. sfx_death.wav       - Comedic downward descending pitch + 8-bit pop (0.35s)
3. sfx_respawn.wav     - Upward magical sparkle / checkpoint spawn arpeggio (0.25s)
4. sfx_stage_clear.wav - Triumphant retro victory fanfare jingle (1.2s)
"""

import os
import math
import struct
import random
import uuid

SAMPLE_RATE = 44100

def pulse_wave(phase, duty=0.5):
    p = phase % 1.0
    return 1.0 if p < duty else -1.0

def triangle_wave(phase):
    p = phase % 1.0
    if p < 0.5:
        return 4.0 * p - 1.0
    else:
        return 3.0 - 4.0 * p

def note_to_freq(note_name):
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    name = note_name[:-1]
    octave = int(note_name[-1])
    semitone = notes.index(name)
    midi = (octave + 1) * 12 + semitone
    return 440.0 * (2.0 ** ((midi - 69) / 12.0))

def export_mono_wav(filepath, samples):
    max_val = max(0.0001, max(abs(s) for s in samples))
    gain = 0.88 / max_val
    total_samples = len(samples)

    with open(filepath, 'wb') as f:
        f.write(b'RIFF')
        f.write(struct.pack('<I', 36 + total_samples * 2))
        f.write(b'WAVE')
        f.write(b'fmt ')
        f.write(struct.pack('<IHHIIHH', 16, 1, 1, SAMPLE_RATE, SAMPLE_RATE * 2, 2, 16))
        f.write(b'data')
        f.write(struct.pack('<I', total_samples * 2))
        
        for s in samples:
            val = math.tanh(s * gain)
            int_val = max(-32767, min(32767, int(val * 32767.0)))
            f.write(struct.pack('<h', int_val))

# 1. JUMP SFX: Rising rapid pitch sweep (160Hz -> 680Hz, 0.12s)
def generate_jump():
    duration = 0.13
    total_samples = int(duration * SAMPLE_RATE)
    samples = []
    phase = 0.0
    for i in range(total_samples):
        t = i / total_samples
        # Exponential pitch rise
        freq = 160.0 * ((680.0 / 160.0) ** (t ** 0.8))
        env = (1.0 - t) ** 0.5
        duty = 0.5 - 0.25 * t
        s = pulse_wave(phase, duty) * env * 0.8
        phase += freq / SAMPLE_RATE
        samples.append(s)
    return samples

# 2. DEATH SFX: Rapid comedic pitch slide down + noise pop (0.35s)
def generate_death():
    duration = 0.38
    total_samples = int(duration * SAMPLE_RATE)
    samples = []
    phase = 0.0
    for i in range(total_samples):
        t = i / total_samples
        # Stepped chromatic drop
        step = int(t * 12)
        base_freq = 480.0 * (0.88 ** step)
        # Vibrato wobble
        freq = base_freq + math.sin(i * 0.08) * 20.0
        env = (1.0 - t) ** 1.2
        
        s = pulse_wave(phase, 0.25) * env * 0.75
        # Add subtle 8-bit noise fizz on impact
        if t < 0.2:
            noise = (random.random() * 2.0 - 1.0) * (0.2 * (1.0 - t / 0.2))
            s += noise
            
        phase += freq / SAMPLE_RATE
        samples.append(s)
    return samples

# 3. RESPAWN SFX: Upward magical sparkle / warp arpeggio (C5 -> E5 -> G5 -> C6 -> E6, 0.28s)
def generate_respawn():
    duration = 0.28
    total_samples = int(duration * SAMPLE_RATE)
    samples = []
    notes = ['C5', 'E5', 'G5', 'C6', 'E6']
    note_dur = total_samples / len(notes)
    phase = 0.0
    for i in range(total_samples):
        note_idx = min(len(notes) - 1, int(i / note_dur))
        freq = note_to_freq(notes[note_idx])
        
        t_in_note = (i % note_dur) / note_dur
        env = (1.0 - t_in_note) ** 0.8
        
        s = pulse_wave(phase, 0.5) * env * 0.7
        # Sub harmonic triangle chime
        s += triangle_wave(phase * 0.5) * env * 0.3
        phase += freq / SAMPLE_RATE
        samples.append(s)
    return samples

# 4. STAGE CLEAR SFX: Triumphant 8-bit Victory Fanfare (1.2s)
def generate_stage_clear():
    duration = 1.3
    total_samples = int(duration * SAMPLE_RATE)
    samples = [0.0] * total_samples
    
    # Fanfare melody: G4 -> C5 -> E5 -> G5 (pause) -> F5 -> G5 -> C6 (hold)
    fanfare = [
        ('G4', 0.0, 0.12),
        ('C5', 0.12, 0.12),
        ('E5', 0.24, 0.12),
        ('G5', 0.36, 0.24),
        ('F5', 0.62, 0.14),
        ('G5', 0.76, 0.14),
        ('C6', 0.90, 0.38)
    ]
    
    for note, start_t, dur_t in fanfare:
        start_i = int(start_t * SAMPLE_RATE)
        dur_i = int(dur_t * SAMPLE_RATE)
        freq = note_to_freq(note)
        phase = 0.0
        for i in range(dur_i):
            idx = start_i + i
            if idx >= total_samples: break
            t = i / dur_i
            env = min(1.0, i / (SAMPLE_RATE * 0.005))
            if t > 0.7:
                env *= (1.0 - t) / 0.3
            
            # Lead pulse with vibrato on sustained notes
            cur_freq = freq
            if dur_t > 0.2 and t > 0.2:
                cur_freq += math.sin((t - 0.2) * 35.0) * (freq * 0.02)
                
            val = pulse_wave(phase, 0.5) * env * 0.6
            # Harmony pulse
            val += pulse_wave(phase * 0.5, 0.25) * env * 0.25
            # Bass support
            val += triangle_wave(phase * 0.25) * env * 0.35
            
            phase += cur_freq / SAMPLE_RATE
            samples[idx] += val

    return samples

if __name__ == '__main__':
    audio_dir = r'Assets/Audio'
    res_dir = r'Assets/Resources/Audio'
    os.makedirs(audio_dir, exist_ok=True)
    os.makedirs(res_dir, exist_ok=True)

    sfx_files = {
        'sfx_jump.wav': generate_jump(),
        'sfx_death.wav': generate_death(),
        'sfx_respawn.wav': generate_respawn(),
        'sfx_stage_clear.wav': generate_stage_clear()
    }

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

    for fname, data in sfx_files.items():
        p1 = os.path.join(audio_dir, fname)
        p2 = os.path.join(res_dir, fname)
        export_mono_wav(p1, data)
        export_mono_wav(p2, data)
        
        g1 = uuid.uuid5(uuid.NAMESPACE_DNS, 'sfx_' + fname).hex
        g2 = uuid.uuid5(uuid.NAMESPACE_DNS, 'res_sfx_' + fname).hex
        with open(p1 + '.meta', 'w', encoding='utf-8') as f:
            f.write(template.format(guid=g1))
        with open(p2 + '.meta', 'w', encoding='utf-8') as f:
            f.write(template.format(guid=g2))

    print('All 4 SFX synthesized and exported to Assets/Audio and Assets/Resources/Audio!')
