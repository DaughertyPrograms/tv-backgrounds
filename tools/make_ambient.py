# Clean Home ambient tracks - 2026-10-26
# Original, fully synthesized loops (no samples, no third-party audio) -> released CC0.
# Every part of each track is periodic over the loop length L (noise built in the frequency domain,
# oscillators on exact k/L frequencies, events and reverb tails wrapped around), so the end flows
# straight back into the start.
import numpy as np, subprocess, os, sys
SR = 44100
L = 240                      # seconds per loop
N = SR * L
rng = np.random.default_rng(7)
t = np.arange(N, dtype=np.float64) / SR
OUT = sys.argv[1] if len(sys.argv) > 1 else "out"

def per(f):                   # snap a frequency to whole cycles per loop
    return max(1, round(f * L)) / L
def lfo(period_div, lo, hi, phase=0.0):
    return lo + (hi - lo) * (0.5 + 0.5 * np.sin(2 * np.pi * t * period_div / L + phase))
def noise(shape_fn, seed):    # periodic coloured noise
    r = np.random.default_rng(seed)
    F = np.fft.rfftfreq(N, 1 / SR)
    spec = (r.normal(size=F.size) + 1j * r.normal(size=F.size)) * shape_fn(np.maximum(F, 1e-3))
    spec[0] = 0
    x = np.fft.irfft(spec, n=N)
    return x / (np.std(x) + 1e-12)
def lp(fc, order=2):  return lambda F: 1 / np.sqrt(1 + (F / fc) ** (2 * order))
def hp(fc, order=2):  return lambda F: 1 / np.sqrt(1 + (fc / F) ** (2 * order))
def bp(f0, q):        return lambda F: 1 / np.sqrt(1 + (q * (F / f0 - f0 / F)) ** 2)
def mul(*fs):         return lambda F: np.prod([f(F) for f in fs], axis=0)
def place(buf, ev, start):   # add an event, wrapping around the loop
    s = int(start) % N; n = len(ev); e = s + n
    if e <= N: buf[s:e] += ev
    else: k = N - s; buf[s:] += ev[:k]; buf[:e - N] += ev[k:]
def reverb(x, secs, seed, damp=3500):   # circular convolution -> tails wrap too
    r = np.random.default_rng(seed); n = int(secs * SR); tt = np.arange(n) / SR
    ir = r.normal(size=n) * np.exp(-6.9 * tt / secs)
    ir = np.fft.irfft(np.fft.rfft(ir) * lp(damp, 1)(np.maximum(np.fft.rfftfreq(n, 1 / SR), 1e-3)), n=n)
    ir /= np.sqrt(np.sum(ir ** 2))
    H = np.fft.rfft(np.concatenate([ir, np.zeros(N - n)]))
    return np.fft.irfft(np.fft.rfft(x) * H, n=N)
def stereo(l, r): return np.stack([l, r], 1)
def pan(x, p):  return stereo(x * np.cos((p + 1) * np.pi / 4), x * np.sin((p + 1) * np.pi / 4))
def env(n, a, r):
    e = np.ones(n); a = int(a * SR); r = int(r * SR)
    if a: e[:a] = np.sin(np.linspace(0, np.pi / 2, a)) ** 2
    if r: e[-r:] *= np.cos(np.linspace(0, np.pi / 2, r)) ** 2
    return e
def note_hz(m): return 440 * 2 ** ((m - 69) / 12)
def pad_voice(freq, dur, a, r, bright=1.6, harm=10, seed=0):
    rr = np.random.default_rng(seed); n = int(dur * SR); tt = np.arange(n) / SR; x = np.zeros(n)
    for h in range(1, harm + 1):
        amp = 1 / h ** bright
        for det in (-0.0018, 0.0021):
            x += amp * np.sin(2 * np.pi * freq * h * (1 + det) * tt + rr.uniform(0, 6.28))
    return x * env(n, a, r)
def finish(name, x, target_db=-24.0):
    x = x - x.mean(0)
    rms = np.sqrt(np.mean(x ** 2)); x *= 10 ** (target_db / 20) / rms
    x = 0.7 * np.tanh(x / 0.7)                       # gentle ceiling, never harsh
    # loudness check after the ceiling
    x *= 10 ** (target_db / 20) / np.sqrt(np.mean(x ** 2))
    pk = np.max(np.abs(x)); assert pk < 0.9, (name, pk)
    jump = np.abs(x[0] - x[-1]).max(); typ = np.median(np.abs(np.diff(x[:SR], axis=0)))
    print(name, "loop seam jump", round(float(jump), 5), "typical step", round(float(typ), 5))
    os.makedirs(os.path.dirname(f"{OUT}/{name}"), exist_ok=True)
    raw = (x * 32767).astype("<i2").tobytes()
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "s16le", "-ar", str(SR), "-ac", "2", "-i", "-",
                    "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart",
                    "-metadata", "title=" + name.split("/")[-1].replace("-", " ").title(),
                    "-metadata", "artist=Clean Home (original, CC0)", "-metadata", "date=2026-10-26",
                    f"{OUT}/{name}.m4a"], input=raw, check=True)
    print(name, "rms dB", round(20 * np.log10(np.sqrt(np.mean(x ** 2))), 1), "peak", round(float(pk), 3))

# ---------------- Nature / Night Field ----------------
def night_field():
    wind = noise(mul(lp(500), hp(60)), 1) * lfo(3, .25, 1) * lfo(7, .6, 1, 1.3)
    wind2 = noise(mul(lp(900), hp(150)), 2) * lfo(5, .2, .8, 2.1)
    L_, R_ = 0.55 * wind + 0.25 * wind2, 0.55 * noise(mul(lp(500), hp(60)), 3) * lfo(3, .25, 1, .4) + 0.25 * wind2
    mix = stereo(L_, R_) * 0.5
    # crickets: short pulse trains at slightly different pitches, each with its own rhythm
    for i, (f, p, period, vol) in enumerate([(4300, -.6, 1.05, .9), (4650, .5, 1.35, .7), (3950, .1, .8, .55), (5100, -.2, 1.7, .4)]):
        c = np.zeros(N); r = np.random.default_rng(20 + i); ts = r.uniform(0, 2)
        pulse_n = int(.016 * SR); pt = np.arange(pulse_n) / SR
        pulse = np.sin(2 * np.pi * f * pt) * np.sin(np.pi * np.arange(pulse_n) / pulse_n) ** 2
        while ts < L:
            if r.random() > .18:                                    # occasional rests
                for k in range(r.integers(2, 5)): place(c, pulse * r.uniform(.7, 1), (ts + k * .034) * SR)
            ts += period * r.uniform(.92, 1.08)
            if r.random() < .03: ts += r.uniform(3, 9)              # a cricket goes quiet for a bit
        c *= lfo(2 + i, .55, 1, i)                                  # swells over minutes
        mix += pan(c * vol * 0.30, p)
    # distant frogs: a few soft low croaks
    frog = np.zeros(N); r = np.random.default_rng(40)
    for _ in range(22):
        n = int(.35 * SR); tt = np.arange(n) / SR
        cro = np.sin(2 * np.pi * 260 * tt + 3 * np.sin(2 * np.pi * 34 * tt)) * (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 17 * tt))) * env(n, .03, .2)
        for k in range(r.integers(1, 4)): place(frog, cro * .5, (r.uniform(0, L) + k * .5) * SR)
    frog = np.fft.irfft(np.fft.rfft(frog) * lp(700, 2)(np.maximum(np.fft.rfftfreq(N, 1 / SR), 1e-3)), n=N)
    mix += pan(frog * .05, .7)
    mix[:, 0] += 0.25 * reverb(mix[:, 0], 2.5, 1); mix[:, 1] += 0.25 * reverb(mix[:, 1], 2.5, 2)
    finish("Nature/night-field", mix, -28.2)

# ---------------- Nature / Gentle Rain ----------------
def gentle_rain():
    base = stereo(noise(mul(lp(2600, 2), hp(250)), 5), noise(mul(lp(2600, 2), hp(250)), 6)) * 0.35
    low = stereo(noise(mul(lp(300), hp(40)), 7), noise(mul(lp(300), hp(40)), 8)) * 0.35 * lfo(4, .5, 1)[:, None]
    mix = base * lfo(3, .7, 1)[:, None] + low
    drops = np.zeros((N, 2)); r = np.random.default_rng(9)
    for _ in range(int(L * 9)):
        f = r.uniform(1800, 4200); n = int(.05 * SR); tt = np.arange(n) / SR
        d = np.sin(2 * np.pi * f * tt * (1 - 2.5 * tt)) * np.exp(-tt / .008)
        p = r.uniform(-1, 1); s = r.uniform(0, L) * SR; v = r.uniform(.05, .22)
        place(drops[:, 0], d * v * np.cos((p + 1) * np.pi / 4), s); place(drops[:, 1], d * v * np.sin((p + 1) * np.pi / 4), s)
    mix += drops * .5
    mix[:, 0] += 0.3 * reverb(mix[:, 0], 1.8, 3); mix[:, 1] += 0.3 * reverb(mix[:, 1], 1.8, 4)
    finish("Nature/gentle-rain", mix, -29.9)

# ---------------- Tech / Soft Tech Drone ----------------
def tech_drone():
    out = np.zeros((N, 2))
    for root, p, vol in [(55, -.3, 1), (82.4, .3, .7), (110, 0, .35)]:
        for side in (0, 1):
            x = np.zeros(N)
            for h in range(1, 24):
                cut = lfo(2 + side, 3, 11, root / 30 + side) if True else 1  # moving "filter"
                amp = (1 / h) / (1 + (h / cut) ** 4)
                det = 1 + (0.0015 if side else -0.0012) * (1 + h * .02)
                x += amp * np.sin(2 * np.pi * per(root * h * det) * t + rng.uniform(0, 6.28))
            out[:, side] += x * vol * (np.cos((p + 1) * np.pi / 4) if side == 0 else np.sin((p + 1) * np.pi / 4))
    out *= lfo(5, .75, 1)[:, None]
    # soft digital shimmer: pentatonic pings with long tails
    pings = np.zeros((N, 2)); r = np.random.default_rng(11); notes = [69, 72, 74, 76, 79, 81, 84]
    ts = 3.0
    while ts < L:
        f = note_hz(notes[r.integers(len(notes))]); n = int(6 * SR); tt = np.arange(n) / SR
        g = (np.sin(2 * np.pi * f * tt) + .3 * np.sin(2 * np.pi * f * 2.003 * tt)) * np.exp(-tt / 1.6) * env(n, .02, 0)
        p = r.uniform(-.8, .8)
        place(pings[:, 0], g * .06 * np.cos((p + 1) * np.pi / 4), ts * SR); place(pings[:, 1], g * .06 * np.sin((p + 1) * np.pi / 4), ts * SR)
        ts += r.uniform(5, 11)
    out += pings
    air = stereo(noise(mul(bp(2500, 1.2)), 12), noise(mul(bp(2500, 1.2)), 13)) * .012 * lfo(3, .3, 1)[:, None]
    out += air
    out[:, 0] += 0.45 * reverb(out[:, 0], 5, 5); out[:, 1] += 0.45 * reverb(out[:, 1], 5, 6)
    finish("Tech/soft-tech-drone", out, -26.5)

# ---------------- Tech / Deep Space ----------------
def deep_space():
    out = np.zeros((N, 2))
    for side in (0, 1):
        x = np.zeros(N)
        for root, v in [(41.2, 1), (61.7, .5), (123.5, .18)]:
            for h in range(1, 10):
                x += (v / h ** 1.8) * np.sin(2 * np.pi * per(root * h * (1 + (.001 if side else -.001))) * t + rng.uniform(0, 6.28))
        out[:, side] = x
    out *= lfo(3, .7, 1)[:, None]
    sweep = stereo(noise(mul(bp(700, 3)), 14), noise(mul(bp(900, 3)), 15)) * .05 * lfo(4, 0, 1)[:, None]
    hiss = stereo(noise(mul(hp(3000), lp(9000)), 16), noise(mul(hp(3000), lp(9000)), 17)) * .006
    out += sweep + hiss
    out[:, 0] += 0.6 * reverb(out[:, 0], 7, 7, 2500); out[:, 1] += 0.6 * reverb(out[:, 1], 7, 8, 2500)
    finish("Tech/deep-space", out, -23.9)

# ---------------- Pads (chord progressions) ----------------
def pad_track(name, chords, secs, bright, extra_bells, seed, db=-25):
    out = np.zeros((N, 2)); r = np.random.default_rng(seed); ts = 0.0; i = 0
    while ts < L - 1e-6:
        ch = chords[i % len(chords)]
        for j, m in enumerate(ch):
            v = pad_voice(note_hz(m), secs + 6, 4.5, 6.0, bright, 9, seed + i * 10 + j) * (0.9 if m < 55 else 0.55)
            p = -0.5 + j / max(1, len(ch) - 1)
            place(out[:, 0], v * np.cos((p + 1) * np.pi / 4), ts * SR); place(out[:, 1], v * np.sin((p + 1) * np.pi / 4), ts * SR)
        if extra_bells:
            for _ in range(2):
                m = ch[r.integers(1, len(ch))] + 12; n = int(7 * SR); tt = np.arange(n) / SR; f = note_hz(m)
                b = (np.sin(2 * np.pi * f * tt) + .25 * np.sin(2 * np.pi * f * 3 * tt) * np.exp(-tt / .4)) * np.exp(-tt / 2.2) * env(n, .01, .5) * .12
                s = (ts + r.uniform(2, secs - 2)) * SR; p = r.uniform(-.6, .6)
                place(out[:, 0], b * np.cos((p + 1) * np.pi / 4), s); place(out[:, 1], b * np.sin((p + 1) * np.pi / 4), s)
        ts += secs; i += 1
    out *= lfo(4, .85, 1)[:, None]
    out = np.stack([np.fft.irfft(np.fft.rfft(out[:, k]) * lp(2600, 1)(np.maximum(np.fft.rfftfreq(N, 1 / SR), 1e-3)), n=N) for k in (0, 1)], 1)
    out[:, 0] += 0.7 * reverb(out[:, 0], 6, seed + 1); out[:, 1] += 0.7 * reverb(out[:, 1], 6, seed + 2)
    finish(name, out, db)

def warm_chords():   # C: Cmaj9 - Am9 - Fmaj9 - Gsus2 (15 s each)
    C = [[36, 48, 52, 55, 59, 62], [33, 45, 48, 52, 55, 59], [29, 41, 45, 48, 52, 55], [31, 43, 45, 50, 55, 57]]
    pad_track("Pads/warm-chords", C, 15, 1.7, True, 100, -27.2)
def evening_glow():  # D: Dmaj7 - Bm9 - Gmaj7 - A6sus (20 s each), softer
    C = [[38, 50, 54, 57, 61], [35, 47, 50, 54, 61], [31, 43, 47, 50, 54], [33, 45, 50, 52, 54]]
    pad_track("Pads/evening-glow", C, 20, 2.1, False, 200, -27.3)

if __name__ == "__main__":
    which = sys.argv[2:] or ["night_field", "gentle_rain", "tech_drone", "deep_space", "warm_chords", "evening_glow"]
    for w in which: globals()[w]()
