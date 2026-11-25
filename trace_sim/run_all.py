"""Run all trace-driven experiments of Section VI (Figs. 4-8) and draw the figures.

    python run_all.py                       # paper settings (can take a few hours)
    python run_all.py --quick               # small run, a few minutes, to check the setup
    python run_all.py --out runs/zipf1 --zipf 1.0 --M 500

Any extra argument is passed to every experiment (see `python exp_central.py --help`).
Arguments an experiment does not use are ignored for that experiment. Figures go to <out>/figs."""
import subprocess, sys, os
EXPS = ['exp_trace.py', 'exp_central.py', 'exp_density.py', 'exp_dec.py', 'exp_learn.py']
here = os.path.dirname(os.path.abspath(__file__))
args = sys.argv[1:]
out = 'runs/quick' if '--quick' in args else 'runs/default'
if '--out' in args:
    out = args[args.index('--out') + 1]
else:
    args += ['--out', out]
for e in EXPS:
    # keep only the options this experiment knows
    helptext = subprocess.run([sys.executable, e, '--help'], cwd=here, capture_output=True, text=True).stdout
    keep, i = [], 0
    while i < len(args):
        a = args[i]; j = i + 1
        while j < len(args) and not args[j].startswith('--'):
            j += 1
        if a.startswith('--') and (a + ' ' in helptext or a + '\n' in helptext):
            keep += args[i:j]
        i = j
    print(f'\n=== {e} {" ".join(keep)}', flush=True)
    subprocess.run([sys.executable, e] + keep, cwd=here, check=True)
subprocess.run([sys.executable, 'rfigs.py', os.path.join(out, 'figs'), out], cwd=here, check=True)
print(f'\nResults and figures are in {os.path.join(here, out)}')
