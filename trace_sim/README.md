# Trace-driven experiments (Section VI-B to VI-F)

Data: Foursquare check-ins of New York and Tokyo (Yang et al., IEEE TSMC 2015),
files `dataset_TSMC2014_NYC.csv` and `dataset_TSMC2014_TKY.csv`
(e.g. from https://github.com/ruslansco/Foursquare-Data-Analysis). Put the two files in `../data/`, or set the environment variable
`FSQ_DIR` to the folder that holds them.

| Script | Output | Paper |
|---|---|---|
| `exp_trace.py` | results/trace.npz | Fig. 4 (trace statistics) |
| `exp_central.py NYC` | results/central_NYC.npz | Fig. 5 (centralized vs. reward) |
| `exp_density.py` | results/density.npz | Fig. 6 (user density, run time) |
| `exp_dec.py` | results/dec.npz | Fig. 7 (decentralized, off-peak price) |
| `exp_learn.py` | results/learn.npz | Fig. 8 (learning from past days) |
| `rfigs.py <outdir>` | PDF figures | Figs. 4-8 |

`core.py` holds the sample-based LP of Section IV-E with the reduction of
Corollary 1, Algorithm 1, the baselines and the potential equilibrium LP.
All LPs are solved by HiGHS (scipy.optimize.linprog), the default solver of
MATLAB linprog, so the MATLAB functions in ../matlab give the same solutions.
The saved .npz files contain every number reported in Section VI.
