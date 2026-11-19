% EXP6_DECENTRALIZED  SP cost at the users' equilibrium versus the
% centralized optimum C*(r) at the same reward, for four selection rules,
% and the solution r'* of (P2) (Fig. 6). N = 6 so that the MILP selections
% are exact.
% lam = 1.2 keeps the demand cap of gen_scenario inactive in most seeds, so
% the caching thresholds differ across seeds and the averages are smooth.
par = default_params(); par.N = 6; par.M = 6; par.lam = 1.2; seeds = 1:30;
rs = 0:0.02:1; R = numel(rs);
keys = {'central', 'best', 'worst', 'fair', 'pot'};
J = zeros(numel(seeds), R, 5); U = J;
for s = seeds
    sc = gen_scenario(par, s); [a, Gm] = user_weights(sc.theta, sc.P);
    pbar = squeeze(sum(a, 2)); CR = sum(pbar(:));
    for k = 1:R
        r = rs(k); rp = 1 - r; X = repmat({zeros(par.N, par.M)}, 1, 5);
        X{1} = central_lp(a, Gm, sc.S, r, [], true);   % fewest copies among optima
        for m = 1:par.M
            am = a(:, :, m);
            X{2}(:, m) = ne_milp(am, Gm, sc.S(m), rp, r, 'best');
            X{3}(:, m) = ne_milp(am, Gm, sc.S(m), rp, r, 'worst');
            X{4}(:, m) = ne_milp(am, Gm, sc.S(m), rp, r, 'fair');
            X{5}(:, m) = potential_ne(am, Gm, sc.S(m), rp);
        end
        for j = 1:5
            J(s, k, j) = sum(sp_cost(X{j}, a, Gm, sc.S, r)) / CR;
            rpj = rp; if j == 1, rpj = -r; end      % centralized: users receive the reward r
            U(s, k, j) = sum(sum(user_payment(X{j}, a, Gm, sc.S, rpj))) / CR;
        end
    end
end
fixedU = true; nS = numel(seeds); save(fullfile('..', 'figs', 'exp6.mat'), '-v7');
mJ = squeeze(mean(J, 1)); mU = squeeze(mean(U, 1));
h = figure('Position', [100 100 760 300]);
% The four selection rules differ by <1%, so the range between the SP-best
% and SP-worst equilibria is drawn as a band, with the fair and potential NE.
Ys = {mJ, mU}; tt = {'(a) SP cost', '(b) User payments'};
yls = {'SP cost C^P / C^R', 'Total user payment / C^R'};
for p = 1:2
    ax = subplot(1, 2, p); hold on; Y = Ys{p};
    lo = min(Y(:, 2), Y(:, 3))'; hi = max(Y(:, 2), Y(:, 3))';
    fill([rs, fliplr(rs)], [lo, fliplr(hi)], [0.85 0.33 0.10], 'FaceAlpha', 0.25, ...
        'EdgeColor', 'none', 'DisplayName', 'SP-best to SP-worst NE');
    plot_method(ax, rs, Y(:, 1), 'central', 9); plot_method(ax, rs, Y(:, 4), 'fair', 9);
    plot_method(ax, rs, Y(:, 5), 'pot', 9);
    xlim([0 1]); xlabel('Reward r = 1 - r'''); ylabel(yls{p}); title(tt{p}); style_axes(ax);
    if p == 1
        [v, i] = min(mJ(:, 5)); plot(ax, rs(i), v, 'kp', 'MarkerFaceColor', 'y', 'MarkerSize', 10, 'DisplayName', 'solution of (P2)');
        ylim([0 2]); add_legend(ax, 'northwest');
    else
        plot(ax, rs, zeros(size(rs)), 'Color', [0.5 0.5 0.5], 'HandleVisibility', 'off'); add_legend(ax, 'southwest');
    end
end
save_fig(h, 'fig_decentralized');
[v, i] = min(mJ(:, 5));
fprintf('exp6: r''*=%.3f (r=%.3f) cost %.4f, centralized at same r %.4f, users %.4f vs %.4f\n', 1 - rs(i), rs(i), v, mJ(i, 1), mU(i, 5), mU(i, 1));
fprintf('exp6 max spread between selections: %.4f\n', max(max(mJ(:, 2:5), [], 2) - min(mJ(:, 2:5), [], 2)));
[~, k] = min(abs(rs - 0.95)); fprintf('exp6 r=0.95 ratio %.3f\n', mJ(k, 3) / mJ(k, 1));
