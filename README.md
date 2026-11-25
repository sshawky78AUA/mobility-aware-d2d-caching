# Mobility-Aware D2D Caching: Simulation Code

Code for the paper

> S. Hosny, "Mobility-Aware D2D Caching: Exact Placement, Selfish Equilibria, and Rewards," submitted to *IEEE Transactions on Mobile Computing*, 2026.

The paper builds on S. Hosny, A. Eryilmaz, A. A. Abouzeid, and H. El Gamal, "On the performance of mobility-aware D2D caching networks," arXiv:1903.10071, 2019.

## Contents

| Folder | Language | What it does | Paper |
|---|---|---|---|
| `matlab/` | MATLAB (also runs in GNU Octave) | Core model: group co-location probabilities, the LP of Theorem 1, greedy whole-copy placement, equilibrium checks, potential equilibrium, the MILP for fair / SP-best / SP-worst equilibria, the worked example and the small-instance experiments | Sections IV-V, Fig. 3, Section VI-A |
| `trace_sim/` | Python | Trace-driven experiments on the Foursquare check-ins of New York and Tokyo, with up to 1000 users and 1000 items | Section VI-B to VI-F, Figs. 4-8 |
| `paper_figs/` | Python | Draws the worked-example and small-instance figures from the `.mat` files written by the MATLAB code | Fig. 3 |

Each folder has its own README with the file list and the mapping between code variables and paper symbols.

## Requirements

- MATLAB R2020b or later with the Optimization Toolbox (`linprog`, `intlinprog`), or GNU Octave 8 or later.
- Python 3.10 or later with the packages in `requirements.txt`:

  ```
  pip install -r requirements.txt
  ```

The LPs in `trace_sim/` are solved by HiGHS through `scipy.optimize.linprog`. HiGHS is also the default solver of MATLAB `linprog`, so both implementations return the same solutions.

## Data

The trace experiments use the Foursquare check-in dataset of Yang et al. (D. Yang, D. Zhang, V. W. Zheng, and Z. Yu, "Modeling user activity preference by leveraging user spatial temporal characteristics in LBSNs," *IEEE Trans. Syst., Man, Cybern.: Syst.*, vol. 45, no. 1, pp. 129-142, 2015). The data is not included here. Download `dataset_TSMC2014_NYC.csv` and `dataset_TSMC2014_TKY.csv` from the dataset authors' page, put them in a folder named `data/` at the top of this repository, or set the environment variable `FSQ_DIR` to the folder that holds them.

## Quick start

```
pip install -r requirements.txt
cd trace_sim
python run_all.py --quick          # every trace experiment with small settings (about 15 s)
```

```matlab
cd matlab
run_all                             % worked example, Table 3, synthetic experiments
```

## Reproducing the results

| Paper result | Code |
|---|---|
| Fig. 3, worked example | `matlab/exp0_example.m` |
| Table 3, coded vs whole-copy placement | `matlab/exp3_gap.m` |
| Fig. 4, trace statistics | `trace_sim/exp_trace.py` |
| Fig. 5, centralized placement vs reward | `trace_sim/exp_central.py` |
| Fig. 6, user density and run time | `trace_sim/exp_density.py` |
| Fig. 7, decentralized placement and pricing | `trace_sim/exp_dec.py` |
| Fig. 8, learning from past days | `trace_sim/exp_learn.py` |

`python trace_sim/run_all.py` runs all trace experiments with the paper settings (this can take a few hours) and draws Figs. 4-8. With the default settings
every script reproduces the saved results exactly. `trace_sim/results/` holds the outputs behind the
paper, so `python rfigs.py figs results` (from `trace_sim/`) redraws Figs. 4-8 without rerunning anything.

## Changing the parameters

The simulations are meant to be rerun with other settings.

- **Python (trace experiments):** every parameter is a command-line option or a JSON entry: city,
  number of users and items, Zipf exponent, request rates, grid cell size, number of popular locations,
  rewards, off-peak prices, number of seeds and sampled days, and more. Run any script with `--help`.
  Examples:

  ```
  python exp_central.py --N 200 --M 500 --zipf 1.0 --out runs/zipf1
  python exp_dec.py --city TKY --kappas 0.5 1.0 --out runs/tokyo
  python run_all.py --out runs/smallcells --cell 250 --L 400
  python rfigs.py runs/zipf1/figs runs/zipf1
  ```

  Each run saves its results and a `params_<script>.json` file with all settings to its own folder,
  so the paper results in `results/` are not overwritten. See `trace_sim/README.md` for the full list.
- **MATLAB:** each experiment file starts with its parameters, and `default_params.m` holds the
  synthetic scenario (users, items, locations, mobility, demand). See `matlab/README.md`.

## Citation

If you use this code, please cite the paper above.

## License

MIT. See `LICENSE`. The Foursquare data keeps its own terms from the dataset authors.
