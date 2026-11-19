"""R5: profiles learned from the last D weekdays before a split date, evaluated on the later (held-out) weekdays."""
import numpy as np, sys
sys.path.insert(0, '.')
from setup import city_data, demand
from profiles import theta
from core import *
D0 = city_data('NYC'); w = D0['w']; L = D0['L']; users = D0['users']; eta = D0['eta']
days = np.sort(w.date.unique()); split = days[int(0.7 * len(days))]
test = w[w.date >= split]; train = w[w.date < split]; tdays = np.sort(train.date.unique())
th_test, _ = theta(test, users, L)
Ds = [5, 10, 20, 40, 80, len(tdays)]; N = 400; M = 1000; T = 12; r = 0.1 / T; seeds = range(3)
res = {k: np.zeros((len(seeds), len(Ds))) for k in ('learned', 'crowd')}; res['oracle'] = np.zeros(len(seeds)); res['local'] = np.zeros(len(seeds))
for si, sd in enumerate(seeds):
    rng = np.random.default_rng(400 + sd); idx = rng.choice(len(users), N, replace=False); P = demand(N, M, rng)
    the = th_test[idx]; Ae, fe = groups_from(sample_snapshots(the, 20, rng), eta)
    def lp_with(th):
        A, f = groups_from(sample_snapshots(th, 5, rng), eta); return central(A, weights(A, f, P), r)
    e = evaluate(lp_with(the), Ae, fe, P, r); res['oracle'][si] = 1 - e['cost'] / e['total']
    e = evaluate((P > r).astype(float), Ae, fe, P, r); res['local'][si] = 1 - e['cost'] / e['total']
    for di, Dd in enumerate(Ds):
        sub = train[train.date >= tdays[-Dd]]; thD, _ = theta(sub, users, L); thD = thD[idx]
        e = evaluate(lp_with(thD), Ae, fe, P, r); res['learned'][si, di] = 1 - e['cost'] / e['total']
        thc = np.repeat(thD.mean(0, keepdims=True), N, 0)
        e = evaluate(lp_with(thc), Ae, fe, P, r); res['crowd'][si, di] = 1 - e['cost'] / e['total']
        print(sd, Dd, round(res['learned'][si, di], 4), round(res['crowd'][si, di], 4), 'oracle', round(res['oracle'][si], 4), 'local', round(res['local'][si], 4), flush=True)
        np.savez('results/learn.npz', Ds=Ds, split=str(split)[:10], **res)
