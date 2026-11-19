function sc = gen_scenario(par, seed)
%GEN_SCENARIO  Synthetic demand and mobility profiles (Section V).
%   Mobility: each user follows the time-inhomogeneous Markov chain of
%   Eq. (3) with transition matrix (1-rho)*I + rho*1*pi_t', which moves the
%   user toward a daily target distribution pi_t. Users belong to
%   communities that share a daytime location and an evening hub.
%   par.disp in [0,1] spreads users over all popular locations (larger
%   disp = fewer meetings). State 1 of the location dimension is the
%   private state 0 of the paper.
%   Demand: Zipf popularity with user-specific perturbation and a common
%   diurnal profile psi_t, so p_{n,t}^m = lam*psi_t*pi_n^m (separable).
rng(seed);
N = par.N; M = par.M; L = par.L; T = par.T; C = par.C;
phase = par.phase;                       % 1x T: 1 home, 2 work, 3 leisure
comm  = mod(0:N-1, C) + 1;               % community of each user
work  = mod(0:C-1, L) + 1;               % daytime location of each community
hub   = L - mod(0:C-1, max(1, L - C)); % evening hub of each community
theta = zeros(T, N, L + 1);
for n = 1:N
    u = gamrnd_simple(ones(1, L)); u = u / sum(u);        % personal preference
    tgt = zeros(T, L + 1);
    for t = 1:T
        switch phase(t)
            case 1   % home
                v = [0.85, 0.15 * u];
            case 2   % work / campus
                pr = 0.10; cw = (1 - par.disp) * 0.80;
                v = [pr, (1 - pr - cw) * u]; v(1 + work(comm(n))) = v(1 + work(comm(n))) + cw;
            otherwise % leisure
                pr = 0.30; ch = (1 - par.disp) * 0.50;
                v = [pr, (1 - pr - ch) * u]; v(1 + hub(comm(n))) = v(1 + hub(comm(n))) + ch;
        end
        tgt(t, :) = v / sum(v);
    end
    th = [1, zeros(1, L)];               % start the warm-up at home
    for day = 1:3                        % reach the cyclo-stationary regime
        for t = 1:T
            Lam = (1 - par.rho) * eye(L + 1) + par.rho * ones(L + 1, 1) * tgt(t, :);
            th = th * Lam;
            if day == 3, theta(t, n, :) = th; end
        end
    end
end
g = (1:M) .^ (-par.zipf); g = g / sum(g);
pref = repmat(g, N, 1) .* exp(par.het * randn(N, M));
pref = pref ./ repmat(sum(pref, 2), 1, M);
psi = par.psi / mean(par.psi);
lam = min(par.lam, 0.95 / (max(psi) * max(pref(:))));
P = zeros(T, N, M);
for t = 1:T, P(t, :, :) = reshape(lam * psi(t) * pref, [1, N, M]); end
sc.theta = theta; sc.P = P; sc.S = ones(1, M); sc.pref = pref; sc.psi = psi;
sc.lam = lam; sc.comm = comm; sc.par = par;
end

function x = gamrnd_simple(k)
% Gamma(k,1) samples for integer-free use without the Statistics Toolbox
% (k = 1 gives exponential samples, enough for a flat Dirichlet).
x = -log(rand(size(k)));
end
