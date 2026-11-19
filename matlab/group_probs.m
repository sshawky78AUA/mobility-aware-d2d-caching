function q = group_probs(theta_t, Gm)
%GROUP_PROBS  Co-location probabilities q_B for one slot.
%   theta_t : N x (L+1) location distribution; column 1 is the "private"
%             state (home/elsewhere) where no D2D sharing is possible,
%             columns 2..L+1 are the L popular locations.
%   Gm      : G x N logical group matrix.
%   q(g) = P(user set Gm(g,:) is exactly the set of users present at one
%   popular location), plus, for singletons, the probability of being in
%   the private state. For every user n: sum over groups containing n = 1.
[G, N] = size(Gm);
th0 = theta_t(:, 1); th = theta_t(:, 2:end); L = size(th, 2);
q = zeros(G, 1);
lth = log(max(th, 1e-300)); l1m = log(max(1 - th, 1e-300));
for l = 1:L
    % log prob that exactly users in g (and nobody else) are at location l
    lp = double(Gm) * lth(:, l) + double(~Gm) * l1m(:, l);
    q = q + exp(lp);
end
single = sum(Gm, 2) == 1;
[~, who] = max(Gm(single, :), [], 2);
q(single) = q(single) + th0(who);
end
