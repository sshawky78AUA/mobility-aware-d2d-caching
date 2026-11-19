function x = potential_ne(am, Gm, S, rp)
%POTENTIAL_NE  Potential-minimizing equilibrium for one item (Theorem 6).
%   Requires separable weights a_{n,B} = abar_n * b_B (Assumption 4).
%   Solves min rp*sum_n x_n/abar_n + sum_B b_B (S - x(B))^+ as an LP.
[N, G] = size(am); abar = sum(am, 2); x = zeros(N, 1);
act = abar > 1e-14;                                % users with no interest never cache
b = zeros(G, 1);
for g = 1:G
    k = find(Gm(g, :) & act', 1);
    if ~isempty(k), b(g) = am(k, g) / abar(k); end
end
keep = b > 1e-15; Gk = double(Gm(keep, act)); bk = b(keep); Gn = size(Gk, 1); Na = sum(act);
f = [rp ./ abar(act); bk];
A = [-Gk, -speye(Gn)]; bb = -S * ones(Gn, 1);
z = lp_solve(f, A, bb, zeros(Na + Gn, 1), [S * ones(Na, 1); inf(Gn, 1)]);
x(act) = min(max(z(1:Na), 0), S);
end
