"""Fig. 6: effect of user density (number of participating users) and LP run time.
Saves <out>/density.npz.  Run with --help for all parameters."""
import numpy as np, time, os
from params import get_params
from setup import city_data, demand
from core import *
p = get_params(dict(cities=['NYC', 'TKY'], Ns=[100, 200, 400, 700, 1000], rho=0.1, seeds=3, seed0=200),
               'User density and run time (Fig. 6)')
Ns = list(p.Ns); M = p.M; T = p.T; rho = p.rho; r = rho / T; seeds = range(p.seeds)
res = {}
for city in p.cities:
    D = city_data(city, p)
    for key in ('LP', 'local', 'nosharing', 'meet', 't'): res[f'{city}_{key}'] = np.zeros((len(seeds), len(Ns)))
    for si, sd in enumerate(seeds):
        for ni, N in enumerate(Ns):
            rng = np.random.default_rng(p.seed0 + sd); idx = rng.choice(len(D['users']), N, replace=False)
            th = D['th'][idx]; eta = D['eta']; P = demand(N, M, rng, p=p)
            loc = sample_snapshots(th, p.K_plan, rng); A, f = groups_from(loc, eta)
            le = sample_snapshots(th, p.K_eval, rng); Ae, fe = groups_from(le, eta)
            meet = np.mean([[(np.bincount(le[k, t], minlength=th.shape[2])[le[k, t]][le[k, t] > 0] >= 2).sum() / N for t in range(T)] for k in range(le.shape[0])])
            W = weights(A, f, P); t0 = time.time(); X = central(A, W, r); tl = time.time() - t0
            e = evaluate(X, Ae, fe, P, r); xl = (P > r).astype(float); el = evaluate(xl, Ae, fe, P, r); en = no_sharing(xl, Ae, fe, P, r)
            for key, v in (('LP', e), ('local', el), ('nosharing', en)): res[f'{city}_{key}'][si, ni] = 1 - v['cost'] / v['total']
            res[f'{city}_meet'][si, ni] = meet; res[f'{city}_t'][si, ni] = tl
            print(city, sd, N, round(res[f'{city}_LP'][si, ni], 4), round(res[f'{city}_local'][si, ni], 4), round(res[f'{city}_nosharing'][si, ni], 4), 'meet %.2f t %.1f' % (meet, tl), flush=True)
            np.savez(os.path.join(p.out, 'density.npz'), Ns=Ns, rho=rho, M=M, **res)
