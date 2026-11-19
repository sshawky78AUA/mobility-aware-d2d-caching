function [x, C] = central_lp(a, Gm, S, r, Z, minCopies)
%CENTRAL_LP  Optimal centralized (MDS-coded) placement.
%   Solves, per item, min r*sum_n x_n + sum_g W_g (S - x(g))^+ , 0<=x<=S,
%   as a linear program. With per-user memory limits Z (N x 1) the items
%   are coupled and solved jointly. With minCopies = true the LP returns,
%   among the optimal placements, one with the fewest cached copies (a tiny
%   extra cost per byte), so that quantities that depend on how much is
%   cached, such as the users' payments, are well defined.
[N, G, M] = size(a);
if nargin < 6 || isempty(minCopies), minCopies = false; end
rr = r + 1e-7 * minCopies;
if nargin < 5 || isempty(Z)
    x = zeros(N, M);
    for m = 1:M
        W = sum(a(:, :, m), 1)';
        keep = W > 1e-14;  Gk = Gm(keep, :);  Wk = W(keep);  Gk_n = size(Gk, 1);
        f = [rr * ones(N, 1); Wk];
        A = [-double(Gk), -speye(Gk_n)];  b = -S(m) * ones(Gk_n, 1);
        z = lp_solve(f, A, b, zeros(N + Gk_n, 1), [S(m) * ones(N, 1); inf(Gk_n, 1)]);
        x(:, m) = min(max(z(1:N), 0), S(m));
    end
else
    nv = M * (N + G); f = zeros(nv, 1); Ai = []; Aj = []; Av = []; b = [];
    lb = zeros(nv, 1); ub = inf(nv, 1); row = 0;
    [gi, gn] = find(Gm);
    for m = 1:M
        off = (m - 1) * (N + G);
        f(off + (1:N)) = rr;  f(off + N + (1:G)) = sum(a(:, :, m), 1)';
        ub(off + (1:N)) = S(m);
        Ai = [Ai; row + gi; row + (1:G)'];  Aj = [Aj; off + gn; off + N + (1:G)'];
        Av = [Av; -ones(numel(gi), 1); -ones(G, 1)];
        b = [b; -S(m) * ones(G, 1)];  row = row + G;
    end
    for n = 1:N   % memory constraints sum_m x_n^m <= Z_n
        Ai = [Ai; (row + 1) * ones(M, 1)];  Aj = [Aj; ((0:M-1) * (N + G) + n)'];
        Av = [Av; ones(M, 1)];  b = [b; Z(n)];  row = row + 1;
    end
    A = sparse(Ai, Aj, Av, row, nv);
    z = lp_solve(f, A, b, lb, ub);
    x = zeros(N, M);
    for m = 1:M, x(:, m) = z((m - 1) * (N + G) + (1:N)); end
end
C = sp_cost(x, a, Gm, S, r);
end
