function [x, val, ok] = ne_milp(am, Gm, S, rp, r, mode)
%NE_MILP  Select an equilibrium of the one-item game by mixed-integer LP.
%   mode = 'best'  : NE with the smallest SP cost  sum_g W_g (S-x(g))^+ + r*sum x
%          'worst' : NE with the largest SP cost
%          'fair'  : NE minimizing max_n x_n / abar_n (proportional fairness),
%                    ties broken toward the smaller SP cost.
%   Binary s_g = 1{x(g) >= S}, e_g = 1{x(g) > S}; uF_n = 1{x_n = S},
%   uZ_n = 1{x_n = 0}. The conditions of Lemma 3 are linear given these.
[N, G0] = size(am); W0 = sum(am, 1)';
keep = W0 > 1e-14; Gm = Gm(keep, :); am = am(:, keep); W = W0(keep); G = size(Gm, 1);
abar = sum(am, 2); Gd = double(Gm); del = 1e-5 * S; BigM = N * S;
% variable layout
ix = 1:N; iu = N + (1:G); is = N + G + (1:G); ie = N + 2*G + (1:G);
iF = N + 3*G + (1:N); iZ = 2*N + 3*G + (1:N); it = 3*N + 3*G + 1; nv = it;
R = struct('i', [], 'j', [], 'v', [], 'b', [], 'n', 0);
for g = 1:G
    mem = find(Gm(g, :));
    R = addrow(R, [ix(mem), iu(g)], [-ones(1, numel(mem)), -1], -S);                  % u >= S - x(g)
    R = addrow(R, [ix(mem), iu(g), is(g)], [ones(1, numel(mem)), 1, -BigM], S);        % u <= S - x(g) + M s
    R = addrow(R, [iu(g), is(g)], [1, S], S);                                          % u <= S (1 - s)
    R = addrow(R, [ix(mem), is(g)], [-ones(1, numel(mem)), S], 0);                     % x(g) >= S s
    R = addrow(R, [ix(mem), is(g)], [ones(1, numel(mem)), -BigM], S - del);           % s=0 -> x(g) <= S - del
    R = addrow(R, [ix(mem), ie(g)], [-ones(1, numel(mem)), S + del], 0);               % e=1 -> x(g) >= S + del
    R = addrow(R, [ix(mem), ie(g)], [ones(1, numel(mem)), -BigM], S);                  % e=0 -> x(g) <= S
    R = addrow(R, [ie(g), is(g)], [1, -1], 0);                                         % e <= s
end
for n = 1:N
    R = addrow(R, [is, iF(n)], [-am(n, :), -abar(n)], rp - abar(n));                 % uF=0 -> D+ <= rp
    R = addrow(R, [ix(n), iF(n)], [-1, S], 0);                                         % uF=1 -> x_n = S
    R = addrow(R, [ie, iZ(n)], [am(n, :), -rp], abar(n) - rp);                         % uZ=0 -> D- >= rp
    R = addrow(R, [ix(n), iZ(n)], [1, S], S);                                          % uZ=1 -> x_n = 0
    if abar(n) > 1e-14
        R = addrow(R, [ix(n), it], [1, -abar(n)], 0);                                  % x_n <= t * abar_n
    else
        R = addrow(R, ix(n), 1, 0);                                                    % no interest -> 0
    end
end
A = sparse(R.i, R.j, R.v, R.n, nv); rhs = R.b;
lb = zeros(nv, 1); ub = [S * ones(N, 1); inf(G, 1); ones(2 * G + 2 * N, 1); inf];
intcon = [is, ie, iF, iZ];
spc = zeros(nv, 1); spc(iu) = W; spc(ix) = r;
switch mode
    case 'best',  f = spc; sense = 1;
    case 'worst', f = spc; sense = -1;
    case 'fair',  f = spc * 1e-4; f(it) = 1; sense = 1;
end
[z, ~, ok] = lp_solve(f, A, rhs, lb, ub, intcon, sense);
if ~ok, x = nan(N, 1); val = nan; return; end
x = min(max(z(ix), 0), S);
val = W' * max(0, S - Gd * x) + r * sum(x);
end

function R = addrow(R, cols, vals, b)
R.n = R.n + 1; k = numel(cols);
R.i = [R.i; R.n * ones(k, 1)]; R.j = [R.j; cols(:)]; R.v = [R.v; vals(:)]; R.b = [R.b; b];
end
