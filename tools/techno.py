"""Synthesises the 'Nachbar von oben' boss track: a loud 132 BPM techno loop (16 bars).

Usage: python techno.py <out.wav>
Original, procedurally generated audio - no samples involved.
"""
import sys
import wave
import numpy as np

SR = 44100
BPM = 132
BEAT = 60 / BPM
BARS = 16
N = int(SR * BEAT * 4 * BARS)
rng = np.random.default_rng(1312)
t_all = np.arange(N) / SR
mix = np.zeros(N)


def place(sig, at_beat, gain=1.0):
    i = int(at_beat * BEAT * SR)
    j = min(N, i + len(sig))
    mix[i:j] += gain * sig[: j - i]


def env(length, decay):
    t = np.arange(int(length * SR)) / SR
    return np.exp(-t / decay)


def lowpass(x, cutoff):
    """one-pole low-pass; cutoff may be an array (per-sample sweep)"""
    a = np.exp(-2 * np.pi * np.broadcast_to(cutoff, x.shape) / SR)
    y = np.empty_like(x)
    acc = 0.0
    for k in range(len(x)):
        acc = (1 - a[k]) * x[k] + a[k] * acc
        y[k] = acc
    return y


def saw(freq, length):
    t = np.arange(int(length * SR)) / SR
    return 2 * ((t * freq) % 1) - 1


# kick: pitch-swept sine with a click, four on the floor
kt = np.arange(int(0.4 * SR)) / SR
kfreq = 45 + 110 * np.exp(-kt / 0.03)
kick = np.sin(2 * np.pi * np.cumsum(kfreq) / SR) * np.exp(-kt / 0.18)
kick[:60] += np.linspace(0.6, 0, 60)

noise = rng.uniform(-1, 1, int(0.3 * SR))
hat_open = np.diff(noise, prepend=0) * env(0.3, 0.06)
hat_closed = np.diff(noise, prepend=0)[: int(0.05 * SR)] * env(0.05, 0.012)
clap_src = lowpass(np.diff(rng.uniform(-1, 1, int(0.25 * SR)), prepend=0), 2500) * env(0.25, 0.05)
clap = clap_src.copy()
for off in (0.011, 0.022):
    s = int(off * SR)
    clap[s:] += clap_src[: len(clap) - s] * 0.8

roots = [55.0, 55.0, 43.65, 49.0]  # A1 A1 F1 G1
for bar in range(BARS):
    for b in range(4):
        beat = bar * 4 + b
        place(kick, beat, 1.0)
        place(hat_open, beat + 0.5, 0.25)
        for s16 in (0.25, 0.75):
            place(hat_closed, beat + s16, 0.12)
        if bar >= 4 and b in (1, 3):
            place(clap, beat, 0.45)
        # rolling bass on the three off-16ths
        root = roots[bar % 4]
        for s16 in (0.25, 0.5, 0.75):
            note = saw(root, BEAT / 4 * 0.9) * env(BEAT / 4 * 0.9, 0.06)
            place(lowpass(note, 600), beat + s16, 0.55)

# acid-ish lead from bar 8: 16th arpeggio through a sweeping filter
lead_notes = [220, 261.63, 329.63, 440, 329.63, 261.63, 220, 196]
lead = np.zeros(N)
start = int(8 * 4 * BEAT * SR)
for k in range(8 * 4 * 4):
    i = start + int(k * BEAT / 4 * SR)
    note = saw(lead_notes[k % len(lead_notes)], BEAT / 4) * env(BEAT / 4, 0.07)
    j = min(N, i + len(note))
    lead[i:j] += note[: j - i]
sweep = 400 + 2600 * (0.5 + 0.5 * np.sin(2 * np.pi * t_all / (BEAT * 16)))
mix += 0.35 * lowpass(lead, sweep)

# sidechain-style pump, then loud: soft clip and normalise to -0.5 dBFS
pump = 1 - 0.35 * np.exp(-((t_all % BEAT) / 0.08))
mix = np.tanh(1.6 * mix * pump)
mix /= np.max(np.abs(mix)) / 0.94

with wave.open(sys.argv[1], 'wb') as w:
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes((mix * 32767).astype('<i2').tobytes())
print(f'{sys.argv[1]}: {N / SR:.1f}s')
