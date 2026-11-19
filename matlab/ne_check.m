function [ok, Dp, Dm] = ne_check(x, a, Gm, S, rp, tol)
%NE_CHECK  Equilibrium conditions of Lemma 3 for one item (x: N x 1).
if nargin < 6, tol = 1e-7; end
N = numel(x); load = double(Gm) * x;              % x(B) for every group
act  = load < S - tol;  actm = load <= S + tol;
Dp = a * act; Dm = a * actm;                      % N x 1
ok = all(~(x < S - tol & Dp > rp + tol)) && all(~(x > tol & Dm < rp - tol));
end
