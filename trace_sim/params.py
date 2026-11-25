"""Shared parameters for the trace-driven experiments.

Every experiment script calls get_params(<its own defaults>, <description>). Any parameter can then be
changed from the command line or from a JSON file, for example

    python exp_central.py --N 200 --M 500 --zipf 1.0 --rhos 0.05 0.1 0.2 --out runs/zipf1
    python exp_central.py --config my_settings.json
    python exp_central.py --quick                      # small, fast run to check the setup

Run any script with --help to see the full list with default values. The defaults reproduce the paper.
The parameters used in a run are saved to <out>/params_<script>.json next to its results.
"""
import argparse, json, os, sys
from types import SimpleNamespace

# Parameters shared by all experiments (Section VI-B of the paper).
COMMON = dict(
    city='NYC',        # 'NYC' (New York) or 'TKY' (Tokyo)
    data_dir='',       # folder with dataset_TSMC2014_{NYC,TKY}.csv ('' = $FSQ_DIR or ../data)
    h0=8,              # first hour of the day that is modeled
    T=12,              # number of one-hour slots per day (h0 ... h0+T-1)
    cell=500,          # side of a grid cell in meters
    L=200,             # number of popular cells kept as D2D locations (all others map to the private state)
    min_days=20,       # keep users with check-ins on at least this many days
    k_user=4.0,        # smoothing weight toward the user's all-day location distribution
    k_pop=4.0,         # smoothing weight toward the population location distribution
    M=1000,            # number of items
    zipf=0.8,          # Zipf exponent of item popularity
    R=12.0,            # mean requests per user per day
    het=0.5,           # lognormal spread of request rates across users
    pers=0.5,          # lognormal personalization of item preferences
    K_plan=5,          # sampled days used to build the placement (sample-based LP, Section IV-E)
    K_eval=20,         # independent sampled days used to evaluate the placement
    out='runs/default' # output folder for this run
)

# Settings used by --quick: small enough to finish in a few minutes on a laptop.
QUICK = dict(N=60, Ns=[30, 60], M=100, seeds=1, rhos=[0.05, 0.2, 0.5], K_eval=5, Ds=[5, 20],
             grid=[0.0, 0.5, 1.0], kappas=[1.0], cities=['NYC'])


def _parser_type(v):
    if isinstance(v, bool):
        return lambda s: str(s).lower() in ('1', 'true', 'yes', 'y')
    if isinstance(v, int):
        return int
    if isinstance(v, float):
        return float
    return str


def get_params(defaults, description):
    D = {**COMMON, **defaults}
    ap = argparse.ArgumentParser(description=description, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    ap.add_argument('--config', default='', help='JSON file with parameter values (command-line values win)')
    ap.add_argument('--quick', action='store_true', help='small, fast run to check the setup')
    for k, v in D.items():
        if isinstance(v, (list, tuple)):
            ap.add_argument('--' + k, type=_parser_type(v[0]), nargs='+', default=None, help=f'default: {list(v)}')
        else:
            ap.add_argument('--' + k, type=_parser_type(v), default=None, help=f'default: {v}')
    a = vars(ap.parse_args())
    P = dict(D)
    if a.pop('quick'):
        P.update({k: v for k, v in QUICK.items() if k in P})
        if P['out'] == COMMON['out']:
            P['out'] = 'runs/quick'
    cfg = a.pop('config')
    if cfg:
        with open(cfg) as fh:
            user = json.load(fh)
        unknown = set(user) - set(D)
        if unknown:
            raise SystemExit(f'Unknown parameters in {cfg}: {sorted(unknown)}')
        P.update(user)
    P.update({k: v for k, v in a.items() if v is not None})
    os.makedirs(P['out'], exist_ok=True)
    name = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    with open(os.path.join(P['out'], f'params_{name}.json'), 'w') as fh:
        json.dump(P, fh, indent=2)
    print('Parameters:', json.dumps(P), flush=True)
    return SimpleNamespace(**P)
