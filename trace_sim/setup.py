"""Scenario construction: users, location profiles, demand. Units: one slot = one busy hour, item size S = 1.
P[n, m] = a_n pi_n^m with p_{n,t}^m = eta_t P[n, m]  (separable, Assumption 4); mean(eta) = 1."""
import numpy as np, sys, os
sys.path.insert(0, '.')
DATA_DIR = os.environ.get('FSQ_DIR', os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data'))
from profiles import load, cells, theta
_cache = {}
def city_data(city, cell=500, L=200, min_days=20):
    k = (city, cell, L, min_days)
    if k not in _cache:
        w = load(os.path.join(DATA_DIR, f'dataset_TSMC2014_{city}.csv')); w['l'] = cells(w, cell, L)
        w.loc[w.venueCategory.str.contains('Home', case=False).values, 'l'] = 0      # at home: private state
        act = w.groupby('userId').date.nunique(); users = np.sort(act[act >= min_days].index.values)
        th, C = theta(w, users, L)
        hourly = np.bincount(w.t.values, minlength=12).astype(float); eta = hourly / hourly.mean()
        days = np.sort(w.date.unique())
        _cache[k] = dict(w=w, users=users, th=th, eta=eta, days=days, L=L)
    return _cache[k]
def demand(N, M, rng, zipf=0.8, R=12.0, het=0.5, pers=0.5, T=12):
    """Requests per user per day ~ R * lognormal(het); preferences = Zipf x lognormal(pers) perturbation."""
    z = np.arange(1, M + 1) ** (-zipf); z /= z.sum()
    pi = z[None, :] * np.exp(pers * rng.standard_normal((N, M))); pi /= pi.sum(1, keepdims=True)
    Rn = R * np.exp(het * rng.standard_normal(N) - het ** 2 / 2)
    return (Rn / T)[:, None] * pi                     # expected requests of item m in an average slot
