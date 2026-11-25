# MATLAB code: Mobility-Aware D2D Caching

Run `run_all` from this folder (Optimization Toolbox: `linprog`, `intlinprog`).

## Changing the parameters

- Each experiment file starts with its parameters (number of users, trials, reward range, ...).
  Edit them and rerun the file, e.g. `exp3_gap` with `Ns = 3:10` or `trials = 1000`.
- `exp0_example` (Fig. 3) takes the interests `p` and the location profiles `th` of the three users at the top.
- `default_params.m` holds the synthetic scenario used by `exp1`-`exp7` (users, items, locations,
  communities, mobility rate, Zipf exponent, demand levels). Changing it changes all of them.
- The core functions (`central_lp`, `greedy_integral`, `potential_ne`, `ne_milp`, ...) take the
  location profiles `theta(t,n,l)` and interests `P(t,n,m)` as inputs, so they can be called on
  any scenario you build.
The code also runs in GNU Octave (falls back to `glpk`). Every experiment saves
its data to `../figs/expN.mat` before plotting.

## Code variables and paper symbols

| Code | Paper |
|---|---|
| `theta(t,n,1)` / `theta(t,n,l+1)` | private-state prob. theta_{n,t}^0 / theta_{n,t}^l |
| `P(t,n,m)` | p_{n,t}^m |
| `Gm` (rows = groups) | groups a in A |
| `q` (group_probs) | q_{a,t}, Eq. (5) |
| `a(n,g,m)` | per-user weights w_{n,a}^m, Eq. (10) |
| `sum(a,1)` | group weights W_a^m |
| `sum(a,2)` | p-hat_n^m |
| `x(n,m)` | x_n^m |
| `r`, `rp` | r, r' = y_o - r (y_o = 1 in the code) |
| `sp_cost` | C^P (and L-bar^P) |
| `user_payment` | mu_n^P |

## Files

| File | Purpose |
|---|---|
| `gen_scenario`, `default_params` | Markov mobility (Eq. 3) and Zipf demand |
| `enum_groups`, `group_probs`, `user_weights` | q_{a,t} and w_{n,a}^m |
| `central_lp` | LP of Theorem 1 (optionally memory limits Z_n, (P1-Z)) |
| `best_integral`, `greedy_integral` | whole-copy placement: exhaustive and Algorithm 1 |
| `saa_weights`, `eval_cost_mc` | sample-based formulation (Section IV-E) |
| `ne_check`, `best_response`, `br_dynamics` | equilibrium conditions (Lemma 3), best-response dynamics |
| `potential_ne` | potential equilibrium (Theorem 5) |
| `ne_milp` | fair / SP-best / SP-worst equilibrium (Proposition 8, Section V-C) |
| `estimate_profiles` | profiles learned from D observed periods |
| `method_style`, `plot_method`, `add_legend`, `style_axes`, `save_fig` | common figure style |
| `exp0_example` | worked example of Section V-E (Fig. 3) |
| `exp3_gap` | Table 3 of the paper (coded versus whole-copy placement, Section VI-A) |
| `exp1`, `exp2`, `exp4` ... `exp7` | additional synthetic experiments with the Markov mobility model (not in the paper) |
