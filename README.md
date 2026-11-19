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

## Reproducing the results

MATLAB (from `matlab/`):

```matlab
run_all          % worked example and small-instance experiments
```

Python (from `trace_sim/`):

```
python exp_trace.py          # Fig. 4, trace statistics
python exp_central.py NYC    # Fig. 5, centralized placement versus reward
python exp_density.py        # Fig. 6, user density and run time
python exp_dec.py            # Fig. 7, decentralized placement and pricing
python exp_learn.py          # Fig. 8, profiles learned from past days
python rfigs.py ../figs      # draws Figs. 4-8 as PDF
```

`trace_sim/results/` holds the saved outputs (`.npz`) behind every number reported in Section VI, so the figures can be redrawn without rerunning the experiments.

## Citation

If you use this code, please cite the paper above.
