# Trace-driven experiments (Section VI-B to VI-F, Figs. 4-8)

These scripts run the full simulations: they build the location profiles from the check-ins, generate
the demand, solve the placement problems (LP, greedy, baselines, potential equilibrium) and evaluate
them on independent sampled days. Plotting is a separate step.

## Data

Foursquare check-ins of New York and Tokyo (Yang et al., IEEE TSMC 2015), files
`dataset_TSMC2014_NYC.csv` and `dataset_TSMC2014_TKY.csv`. Put the two files in `../data/`, or set the
environment variable `FSQ_DIR` (or the option `--data_dir`) to the folder that holds them.

## Running

```
python run_all.py --quick        # all experiments with small settings, about 15 s, to check the setup
python run_all.py                # all experiments with the paper settings (can take a few hours)
python exp_central.py            # one experiment, paper settings
python rfigs.py figs results     # redraw Figs. 4-8 from the saved paper results
```

| Script | Output | Paper |
|---|---|---|
| `exp_trace.py` | trace.npz | Fig. 4 (trace statistics) |
| `exp_central.py` | central_<city>.npz | Fig. 5 (centralized placement versus reward) |
| `exp_density.py` | density.npz | Fig. 6 (user density, run time) |
| `exp_dec.py` | dec.npz | Fig. 7 (decentralized placement, off-peak price) |
| `exp_learn.py` | learn.npz | Fig. 8 (learning from past days) |
| `rfigs.py <figs> <results>` | PDF figures | Figs. 4-8 |
| `run_all.py` | all of the above | |

Each run writes its results to the folder given by `--out` (default `runs/default`, or `runs/quick`
with `--quick`), together with a `params_<script>.json` file listing every parameter used. The folder
`results/` holds the runs behind the paper and is never overwritten unless you pass `--out results`.

## Changing the parameters

Every parameter can be set on the command line or in a JSON file. Run any script with `--help` to see
the full list and the defaults, which are the paper settings.

```
python exp_central.py --N 200 --M 500 --zipf 1.0 --out runs/zipf1
python exp_central.py --city TKY --rhos 0.05 0.1 0.2 --seeds 2 --out runs/tokyo
python exp_dec.py --kappas 0.5 1.0 --grid 0 0.2 0.4 0.6 0.8 1 --out runs/dec
python exp_density.py --Ns 100 300 500 --cell 250 --L 400 --out runs/smallcells
python exp_learn.py --Ds 5 10 20 0 --split_frac 0.6 --out runs/learn
python exp_central.py --config my_settings.json
python run_all.py --out runs/zipf1 --zipf 1.0     # all experiments with one change
python rfigs.py runs/zipf1/figs runs/zipf1        # plot your own run
```

A JSON file holds any subset of the parameters, e.g. `{"N": 300, "zipf": 1.0, "rhos": [0.05, 0.1]}`;
command-line values override it.

Shared parameters (all scripts, see `params.py`):

| Option | Default | Meaning |
|---|---|---|
| `--city` | NYC | NYC or TKY |
| `--data_dir` | `../data` | folder with the check-in files |
| `--h0`, `--T` | 8, 12 | first hour and number of one-hour slots per day |
| `--cell`, `--L` | 500, 200 | grid cell size (m) and number of popular cells |
| `--min_days` | 20 | keep users active on at least this many weekdays |
| `--k_user`, `--k_pop` | 4, 4 | smoothing weights of the location profiles |
| `--M` | 1000 | number of items |
| `--zipf` | 0.8 | Zipf exponent of item popularity |
| `--R`, `--het`, `--pers` | 12, 0.5, 0.5 | requests per user per day, spread across users, personalization |
| `--K_plan`, `--K_eval` | 5, 20 | sampled days used to plan and to evaluate |
| `--out` | runs/default | output folder |

Experiment parameters:

| Script | Options (defaults) |
|---|---|
| `exp_trace.py` | `--cities` (NYC TKY), `--Ns` (200 400 1000), `--seed` (7) |
| `exp_central.py` | `--N` (400), `--rhos` (0.02 ... 1.0), `--seeds` (4), `--methods` (LP greedy pairwise crowd popularity local nosharing) |
| `exp_density.py` | `--cities` (NYC TKY), `--Ns` (100 200 400 700 1000), `--rho` (0.1), `--seeds` (3) |
| `exp_dec.py` | `--N` (400), `--kappas` (0.4 0.7 1.0), `--grid` (0, 0.1, ..., 1), `--seeds` (2) |
| `exp_learn.py` | `--N` (400), `--Ds` (5 10 20 40 80 0, where 0 = all training days), `--rho` (0.1), `--split_frac` (0.7), `--seeds` (3) |

The reward is given as rho = rT (reward per item-day, in off-peak units) and the off-peak price as
kappa = y_o T, as in Section VI-B. `--seed0` sets the first random seed of each experiment.

## Code

`core.py` holds the sample-based LP of Section IV-E with the reduction of Corollary 1, Algorithm 1
(greedy), the baselines (pairwise contacts, crowd mobility, popularity, local caching, no sharing) and
the potential-equilibrium LP of Section V. `profiles.py` builds the location profiles and `setup.py`
the users and the demand. All LPs are solved by HiGHS (`scipy.optimize.linprog`), the default solver of
MATLAB `linprog`, so the MATLAB functions in `../matlab` give the same solutions.

With the default settings the scripts reproduce the numbers saved in `results/` exactly.
