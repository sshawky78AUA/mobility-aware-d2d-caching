"""Fig. 7: decentralized placement (potential equilibrium) versus centralized, for several off-peak prices.
Saves <out>/dec.npz.  Run with --help for all parameters.

kappas are off-peak prices per item-day, kappa = y_o*T; grid is the reward as a fraction of y_o (r = g*y_o)."""
import numpy as np, os
from params import get_params
from setup import city_data, demand
from core import *
p = get_params(dict(N=400, seeds=2, seed0=300, kappas=[0.4, 0.7, 1.0], grid=list(np.round(np.linspace(0.0, 1.0, 11), 2))),
               'Decentralized versus centralized placement (Fig. 7)')
N = p.N; M = p.M; T = p.T; seeds = range(p.seeds); kappas = list(p.kappas); grid = np.array(p.grid, float)
D = city_data(p.city, p); res = {}
for kap in kappas:
    res[f'C_{kap}'] = np.zeros((len(seeds), len(grid))); res[f'P_{kap}'] = np.zeros_like(res[f'C_{kap}'])
for si, sd in enumerate(seeds):
    rng = np.random.default_rng(p.seed0 + sd); idx = rng.choice(len(D['users']), N, replace=False)
    th = D['th'][idx]; eta = D['eta']; P = demand(N, M, rng, p=p)
    A, f = groups_from(sample_snapshots(th, p.K_plan, rng), eta); Ae, fe = groups_from(sample_snapshots(th, p.K_eval, rng), eta); W = weights(A, f, P)
    for kap in kappas:
        yo = kap / T
        for gi, g in enumerate(grid):
            r = g * yo; rp = yo - r
            Xc = central(A, W, r)
            Xp = np.column_stack([pot_item(A, f, P[:, m], rp) for m in range(M)])
            ec = evaluate(Xc, Ae, fe, P, r); ep = evaluate(Xp, Ae, fe, P, r)
            res[f'C_{kap}'][si, gi] = ec['cost'] / ec['total']; res[f'P_{kap}'][si, gi] = ep['cost'] / ep['total']
            print(sd, kap, round(g, 2), round(res[f'C_{kap}'][si, gi], 4), round(res[f'P_{kap}'][si, gi], 4), flush=True)
        np.savez(os.path.join(p.out, 'dec.npz'), grid=grid, kappas=kappas, **res)
