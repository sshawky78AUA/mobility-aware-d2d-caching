"""Fig. 8: profiles learned from the last D weekdays before a split date, evaluated on the later
(held-out) weekdays. Saves <out>/learn.npz.  Run with --help for all parameters.
Ds = 0 stands for all training days."""
import numpy as np, os
from params import get_params
from setup import city_data, demand
from profiles import theta
from core import *
p = get_params(dict(N=400, seeds=3, seed0=400, rho=0.1, split_frac=0.7, Ds=[5, 10, 20, 40, 80, 0]),
               'Learning the profiles from past days (Fig. 8)')
D0 = city_data(p.city, p); w = D0['w']; L = D0['L']; users = D0['users']; eta = D0['eta']
days = np.sort(w.date.unique()); split = days[int(p.split_frac * len(days))]
test = w[w.date >= split]; train = w[w.date < split]; tdays = np.sort(train.date.unique())
th_test, _ = theta(test, users, L, p.T, p.k_user, p.k_pop)
Ds = [d if d > 0 else len(tdays) for d in p.Ds]; N = p.N; M = p.M; T = p.T; r = p.rho / T; seeds = range(p.seeds)
res = {k: np.zeros((len(seeds), len(Ds))) for k in ('learned', 'crowd')}; res['oracle'] = np.zeros(len(seeds)); res['local'] = np.zeros(len(seeds))
for si, sd in enumerate(seeds):
    rng = np.random.default_rng(p.seed0 + sd); idx = rng.choice(len(users), N, replace=False); P = demand(N, M, rng, p=p)
    the = th_test[idx]; Ae, fe = groups_from(sample_snapshots(the, p.K_eval, rng), eta)
    def lp_with(th):
        A, f = groups_from(sample_snapshots(th, p.K_plan, rng), eta); return central(A, weights(A, f, P), r)
    e = evaluate(lp_with(the), Ae, fe, P, r); res['oracle'][si] = 1 - e['cost'] / e['total']
    e = evaluate((P > r).astype(float), Ae, fe, P, r); res['local'][si] = 1 - e['cost'] / e['total']
    for di, Dd in enumerate(Ds):
        sub = train[train.date >= tdays[-min(Dd, len(tdays))]]; thD, _ = theta(sub, users, L, p.T, p.k_user, p.k_pop); thD = thD[idx]
        e = evaluate(lp_with(thD), Ae, fe, P, r); res['learned'][si, di] = 1 - e['cost'] / e['total']
        thc = np.repeat(thD.mean(0, keepdims=True), N, 0)
        e = evaluate(lp_with(thc), Ae, fe, P, r); res['crowd'][si, di] = 1 - e['cost'] / e['total']
        print(sd, Dd, round(res['learned'][si, di], 4), round(res['crowd'][si, di], 4), 'oracle', round(res['oracle'][si], 4), 'local', round(res['local'][si], 4), flush=True)
        np.savez(os.path.join(p.out, 'learn.npz'), Ds=Ds, split=str(split)[:10], **res)
