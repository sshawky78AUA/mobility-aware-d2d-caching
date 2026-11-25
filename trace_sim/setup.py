"""Scenario construction: users, location profiles, demand. Units: one slot = one busy hour, item size S = 1.
P[n, m] = a_n pi_n^m with p_{n,t}^m = eta_t P[n, m]  (separable, Assumption 4); mean(eta) = 1."""
import numpy as np, os
from profiles import load, cells, theta
_cache = {}


def data_dir(p=None):
    d = getattr(p, 'data_dir', '') if p is not None else ''
    return d or os.environ.get('FSQ_DIR', os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data'))


def city_data(city, p=None, cell=500, L=200, min_days=20, h0=8, T=12, k_user=4.0, k_pop=4.0):
    """Location profiles theta[n, t, l] of the active users of a city. Pass the parameter object p
    (from params.get_params) to use its settings; otherwise the paper defaults are used."""
    if p is not None:
        cell, L, min_days, h0, T, k_user, k_pop = p.cell, p.L, p.min_days, p.h0, p.T, p.k_user, p.k_pop
    k = (city, cell, L, min_days, h0, T, k_user, k_pop, data_dir(p))
    if k not in _cache:
        path = os.path.join(data_dir(p), f'dataset_TSMC2014_{city}.csv')
        if not os.path.exists(path):
            raise SystemExit(f'Missing {path}. Download the Foursquare data (see README) or set --data_dir / FSQ_DIR.')
        w = load(path, h0, T); w['l'] = cells(w, cell, L)
        w.loc[w.venueCategory.str.contains('Home', case=False).values, 'l'] = 0      # at home: private state
        act = w.groupby('userId').date.nunique(); users = np.sort(act[act >= min_days].index.values)
        th, C = theta(w, users, L, T, k_user, k_pop)
        hourly = np.bincount(w.t.values, minlength=T).astype(float); eta = hourly / hourly.mean()
        days = np.sort(w.date.unique())
        _cache[k] = dict(w=w, users=users, th=th, eta=eta, days=days, L=L, T=T, h0=h0)
    return _cache[k]


def demand(N, M, rng, zipf=0.8, R=12.0, het=0.5, pers=0.5, T=12, p=None):
    """Requests per user per day ~ R * lognormal(het); preferences = Zipf x lognormal(pers) perturbation.
    Returns the expected requests of item m by user n in an average slot."""
    if p is not None:
        zipf, R, het, pers, T = p.zipf, p.R, p.het, p.pers, p.T
    z = np.arange(1, M + 1) ** (-zipf); z /= z.sum()
    pi = z[None, :] * np.exp(pers * rng.standard_normal((N, M))); pi /= pi.sum(1, keepdims=True)
    Rn = R * np.exp(het * rng.standard_normal(N) - het ** 2 / 2)
    return (Rn / T)[:, None] * pi
