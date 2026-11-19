"""R4: decentralized placement (potential equilibrium) versus centralized, for several off-peak prices."""
import numpy as np, time, sys
sys.path.insert(0, '.')
from setup import city_data, demand
from core import *
N = 400; M = 1000; T = 12; seeds = range(2); kappas = [0.4, 0.7, 1.0]
grid = np.linspace(0.0, 1.0, 11)              # reward as a fraction of the off-peak price
D = city_data('NYC'); res = {}
for kap in kappas:
    res[f'C_{kap}'] = np.zeros((len(seeds), len(grid))); res[f'P_{kap}'] = np.zeros_like(res[f'C_{kap}'])
for si, sd in enumerate(seeds):
    rng = np.random.default_rng(300 + sd); idx = rng.choice(len(D['users']), N, replace=False)
    th = D['th'][idx]; eta = D['eta']; P = demand(N, M, rng)
    A, f = groups_from(sample_snapshots(th, 5, rng), eta); Ae, fe = groups_from(sample_snapshots(th, 20, rng), eta); W = weights(A, f, P)
    for kap in kappas:
        yo = kap / T
        for gi, g in enumerate(grid):
            r = g * yo; rp = yo - r
            Xc = central(A, W, r)
            Xp = np.column_stack([pot_item(A, f, P[:, m], rp) for m in range(M)])
            ec = evaluate(Xc, Ae, fe, P, r); ep = evaluate(Xp, Ae, fe, P, r)
            res[f'C_{kap}'][si, gi] = ec['cost'] / ec['total']; res[f'P_{kap}'][si, gi] = ep['cost'] / ep['total']
            print(sd, kap, round(g, 2), round(res[f'C_{kap}'][si, gi], 4), round(res[f'P_{kap}'][si, gi], 4), flush=True)
        np.savez('results/dec.npz', grid=grid, kappas=kappas, **res)
