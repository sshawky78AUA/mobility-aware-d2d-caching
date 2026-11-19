"""R3: effect of user density (number of participating users) in NYC and Tokyo, and LP run time."""
import numpy as np, time, sys
sys.path.insert(0, '.')
from setup import city_data, demand
from core import *
Ns = [100, 200, 400, 700, 1000]; M = 1000; T = 12; rho = 0.1; r = rho / T; seeds = range(3)
res = {}
for city in ('NYC', 'TKY'):
    D = city_data(city)
    for key in ('LP', 'local', 'nosharing', 'meet', 't'): res[f'{city}_{key}'] = np.zeros((len(seeds), len(Ns)))
    for si, sd in enumerate(seeds):
        for ni, N in enumerate(Ns):
            rng = np.random.default_rng(200 + sd); idx = rng.choice(len(D['users']), N, replace=False)
            th = D['th'][idx]; eta = D['eta']; P = demand(N, M, rng)
            loc = sample_snapshots(th, 5, rng); A, f = groups_from(loc, eta)
            le = sample_snapshots(th, 20, rng); Ae, fe = groups_from(le, eta)
            occ = np.zeros(le.shape[:2] + (th.shape[2],))
            meet = np.mean([[(np.bincount(le[k, t], minlength=th.shape[2])[le[k, t]][le[k, t] > 0] >= 2).sum() / N for t in range(T)] for k in range(le.shape[0])])
            W = weights(A, f, P); t0 = time.time(); X = central(A, W, r); tl = time.time() - t0
            e = evaluate(X, Ae, fe, P, r); xl = (P > r).astype(float); el = evaluate(xl, Ae, fe, P, r); en = no_sharing(xl, Ae, fe, P, r)
            for key, v in (('LP', e), ('local', el), ('nosharing', en)): res[f'{city}_{key}'][si, ni] = 1 - v['cost'] / v['total']
            res[f'{city}_meet'][si, ni] = meet; res[f'{city}_t'][si, ni] = tl
            print(city, sd, N, round(res[f'{city}_LP'][si, ni], 4), round(res[f'{city}_local'][si, ni], 4), round(res[f'{city}_nosharing'][si, ni], 4), 'meet %.2f t %.1f' % (meet, tl), flush=True)
            np.savez('results/density.npz', Ns=Ns, rho=rho, **res)
