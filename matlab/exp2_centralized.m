% EXP2_CENTRALIZED  SP saving versus the reward r (exact weights, N = 8), Fig. 3.
par = default_params(); seeds = 1:20; rs = 0:0.01:0.6; R = numel(rs);
keys = {'lp', 'whole', 'greedy', 'crowd', 'nod2d'};
Cn = zeros(numel(seeds), R, 5); Xc = zeros(numel(seeds), R, 3);
for s = seeds
    sc = gen_scenario(par, s); [a, Gm] = user_weights(sc.theta, sc.P);
    pbar = squeeze(sum(a, 2)); CR = sum(sc.S .* sum(pbar, 1));
    thc = repmat(mean(sc.theta, 2), [1 par.N 1]); ac = user_weights(thc, sc.P, Gm);   % crowd baseline
    for k = 1:R
        r = rs(k);
        X = {central_lp(a, Gm, sc.S, r), best_integral(a, Gm, sc.S, r), greedy_integral(a, Gm, sc.S, r), ...
             central_lp(ac, Gm, sc.S, r), sc.S(1) * double(pbar > r)};
        for j = 1:5, Cn(s, k, j) = sum(sp_cost(X{j}, a, Gm, sc.S, r)) / CR; end
        Xc(s, k, :) = [sum(X{1}(:)), sum(X{4}(:)), sum(X{5}(:))] / par.M;
    end
end
save(fullfile('..', 'figs', 'exp2.mat'), '-v7');
mC = 1 - squeeze(mean(Cn, 1)); mX = squeeze(mean(Xc, 1));      % saving Delta C / C^R
h = figure('Position', [100 100 760 300]);
ax = subplot(1, 2, 1); hold on;
for j = 1:5, plot_method(ax, rs, mC(:, j), keys{j}); end
xlabel('Reward r'); ylabel('SP saving \DeltaC / C^R'); add_legend(ax, 'northeast');
title('(a) SP saving'); style_axes(ax);
ax = subplot(1, 2, 2); hold on; kk = {'lp', 'crowd', 'nod2d'};
for j = 1:3, plot_method(ax, rs, max(mX(:, j), 1e-3), kk{j}); end
set(ax, 'YScale', 'log'); ylim([1e-2 10]);
xlabel('Reward r'); ylabel('Copies per item'); add_legend(ax, 'northeast');
title('(b) Total placement X^*(r)/M'); style_axes(ax);
save_fig(h, 'fig_central_r');
for r0 = [0.2 0.4]
    k = find(abs(rs - r0) < 1e-9); fprintf('exp2 r=%.1f: ', r0); fprintf('%.4f ', mC(k, :)); fprintf('\n');
end
