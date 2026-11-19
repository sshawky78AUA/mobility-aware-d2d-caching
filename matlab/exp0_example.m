% EXP0_EXAMPLE  Worked example (Fig. 3): one item, three users, T = 1.
%   (a) centralized LP placement x_n^*(r) and the thresholds r_1, r_N;
%   (b) decentralized equilibria versus r' (fair, potential, SP-best/worst)
%       and the validity of the earlier proportional rule;
%   (c) SP cost of both schemes on a common reward axis, y_o = 1.
clear; S = 1; N = 3; yo = 1;
p  = [0.5 0.4 0.3];                       % interests p_n (T = 1)
th = [0.2 0.6 0.2; 0.1 0.5 0.4; 0.2 0.3 0.5];   % [private, C, D] per user
Gm = enum_groups(N);
theta = reshape(th, [1 N 3]); P = reshape(p, [1 N 1]);
[a, Gm] = user_weights(theta, P, Gm); am = a(:, :, 1); W = sum(am, 1)';
tau = arrayfun(@(n) am(n, find(Gm(:, n) & sum(Gm, 2) == 1)), 1:N);   % p-tilde_n
sn  = double(Gm)' * W;                                               % level-1 scores s_n
phat = sum(am, 2)';
spc = @(x, r) W' * max(S - double(Gm) * x(:), 0) + r * sum(x);       % SP cost of one item
fprintf('tau = %s, s = %s, phat = %s\n', mat2str(tau, 3), mat2str(sn', 3), mat2str(phat, 3));

% (a) centralized
rs = 0:0.005:0.8; Xc = zeros(N, numel(rs)); Cc = zeros(1, numel(rs));
for k = 1:numel(rs)
    [x, C] = central_lp(a, Gm, S, rs(k), [], true); Xc(:, k) = x; Cc(k) = C;
end
% (b) decentralized
rps = 0:0.005:0.6; nr = numel(rps);
Xf = zeros(N, nr); Xp = Xf; Xb = Xf; Xw = Xf; propOK = true(1, nr); multi = false(1, nr);
for k = 1:nr
    rp = rps(k); r = yo - rp;
    Xf(:, k) = ne_milp(am, Gm, S, rp, r, 'fair');
    Xb(:, k) = ne_milp(am, Gm, S, rp, r, 'best');
    Xw(:, k) = ne_milp(am, Gm, S, rp, r, 'worst');
    Xp(:, k) = potential_ne(am, Gm, S, rp);
    multi(k) = norm(Xb(:, k) - Xw(:, k)) > 1e-6 || norm(Xf(:, k) - Xp(:, k)) > 1e-6;
    % earlier proportional rule
    xr = zeros(N, 1); full = rp < tau; none = rp >= phat; mid = ~full & ~none;
    xr(full) = S; if any(mid), xr(mid) = S * phat(mid) / sum(phat(mid)); end
    propOK(k) = ne_check(xr, am, Gm, S, rp);
end
% (c) SP cost on a common reward axis
rr = 0:0.005:1; CP = zeros(3, numel(rr)); CR = S * sum(phat);
for k = 1:numel(rr)
    r = rr(k); rp = yo - r;
    CP(1, k) = spc(central_lp(a, Gm, S, r, [], true), r);
    CP(2, k) = spc(ne_milp(am, Gm, S, rp, r, 'fair'), r);
    CP(3, k) = spc(potential_ne(am, Gm, S, rp), r);
end
CP = CP / CR;
save(fullfile('..', 'figs', 'exp0.mat'), 'p', 'th', 'tau', 'sn', 'phat', 'rs', 'Xc', 'rps', ...
     'Xf', 'Xp', 'Xb', 'Xw', 'propOK', 'multi', 'rr', 'CP', 'yo', '-v7');

% ---- plot ----
plot_example(fullfile('..', 'figs', 'exp0.mat'));
