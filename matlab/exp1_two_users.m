% EXP1_TWO_USERS  Equilibria of the two-user game (Fig. 2): p = (0.8, 0.6),
% the users meet with probability 0.5, T = 1, no private state.
th = zeros(1, 2, 3); th(1, :, 2:3) = 0.5; P = reshape([0.8 0.6], [1 2 1]);
[a, Gm] = user_weights(th, P); am = a(:, :, 1); S = 1;
rps = 0:0.0025:1; K = numel(rps);
xf = zeros(2, K); xp = xf; xlo = xf; xhi = xf; muf = xf; mup = xf;
for k = 1:K
    rp = rps(k); r = 1 - rp;
    xf(:, k) = ne_milp(am, Gm, S, rp, r, 'fair');
    xp(:, k) = potential_ne(am, Gm, S, rp);
    xa = ne_milp(am, Gm, S, rp, r, 'best'); xb = ne_milp(am, Gm, S, rp, r, 'worst');
    xlo(:, k) = min(xa, xb); xhi(:, k) = max(xa, xb);
    muf(:, k) = user_payment(xf(:, k), a, Gm, S, rp); mup(:, k) = user_payment(xp(:, k), a, Gm, S, rp);
end
multi = any(abs(xhi - xlo) > 1e-6, 1);
multi = multi & ([multi(2:end) false] | [false multi(1:end-1)]);   % drop threshold ties
save(fullfile('..', 'figs', 'exp1.mat'), '-v7');
% plot: break lines at the jumps so that they are drawn as vertical steps
brk = @(y) [y(1), reshape([y(2:end); nan(1, numel(y) - 1)], 1, [])];
h = figure('Position', [100 100 760 300]); cl = {[0.85 0.33 0.10], [0 0.45 0.74]};
ax = subplot(1, 2, 1); hold on; idx = find(multi);
patch([rps(idx(1)) rps(idx(end)) rps(idx(end)) rps(idx(1))], [-0.05 -0.05 1.05 1.05], [0.9 0.9 0.9], 'EdgeColor', 'none');
for n = 1:2
    stairs(rps, xf(n, :), '-', 'Color', cl{n}, 'LineWidth', 1.6);
    stairs(rps, xp(n, :), '--', 'Color', cl{n}, 'LineWidth', 1.2);
end
xlabel('Caching cost r'''); ylabel('x_n^m / S_m'); ylim([-0.05 1.05]);
legend({'multiple NE', 'x_1 fair', 'x_1 potential', 'x_2 fair', 'x_2 potential'}, 'Location', 'west', 'FontSize', 8);
title('(a) Equilibrium placement'); style_axes(ax);
ax = subplot(1, 2, 2); hold on;
for n = 1:2   % NaN at the jumps so that discontinuities are not drawn as lines
    [xb, yb] = break_jumps(rps, muf(n, :)); plot(xb, yb, '-', 'Color', cl{n}, 'LineWidth', 1.6);
    [xb, yb] = break_jumps(rps, mup(n, :)); plot(xb, yb, '--', 'Color', cl{n}, 'LineWidth', 1.2);
end
yl = [-0.03 0.9]; patch([rps(idx(1)) rps(idx(end)) rps(idx(end)) rps(idx(1))], yl([1 1 2 2]), [0.9 0.9 0.9], ...
    'EdgeColor', 'none', 'HandleVisibility', 'off');
c = get(ax, 'Children'); set(ax, 'Children', [c(2:end); c(1)]); ylim(yl);   % shading behind the curves
xlabel('Caching cost r'''); ylabel('Expected payment \mu_n^P');
legend({'\mu_1 fair', '\mu_1 potential', '\mu_2 fair', '\mu_2 potential'}, 'Location', 'northwest', 'FontSize', 8);
title('(b) User payments'); style_axes(ax);
save_fig(h, 'fig_two_users');
fprintf('exp1: multiple NE for r'' in [%.3f, %.3f]\n', rps(idx(1)), rps(idx(end)));

