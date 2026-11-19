% EXP4_MOBILITY  Impact of mobility (Fig. 4): dispersion delta of users over
% the popular locations (delta = 0: communities stay together; delta = 1:
% everybody follows a personal preference). Centralized placement, r = 0.2.
par = default_params(); ds = 0:0.1:1; seeds = 1:20; r = 0.2;
sav = zeros(numel(seeds), numel(ds), 3); cop = sav; meet = zeros(numel(seeds), numel(ds));
for s = seeds
    for i = 1:numel(ds)
        par.disp = ds(i); sc = gen_scenario(par, s); [a, Gm] = user_weights(sc.theta, sc.P);
        pbar = squeeze(sum(a, 2)); CR = sum(pbar(:));
        single = sum(Gm, 2) == 1; v = zeros(par.N, 1);
        for n = 1:par.N, v(n) = 1 - sum(a(n, single & Gm(:, n), 1)) / pbar(n, 1); end
        meet(s, i) = mean(v);
        thc = repmat(mean(sc.theta, 2), [1 par.N 1]);
        X = {central_lp(a, Gm, sc.S, r), double(pbar > r), central_lp(user_weights(thc, sc.P, Gm), Gm, sc.S, r)};
        for j = 1:3
            sav(s, i, j) = 1 - sum(sp_cost(X{j}, a, Gm, sc.S, r)) / CR;
            cop(s, i, j) = sum(X{j}(:)) / par.M;
        end
    end
end
save(fullfile('..', 'figs', 'exp4.mat'), '-v7');
mS = squeeze(mean(sav, 1)); mC = squeeze(mean(cop, 1)); mv = mean(meet, 1);
keys = {'lp', 'nod2d', 'crowd'};
h = figure('Position', [100 100 760 300]);
ax = subplot(1, 2, 1); hold on;
for j = 1:3, plot_method(ax, ds, mS(:, j), keys{j}, 11); end
xlabel('Dispersion \delta'); ylabel('SP saving \DeltaC / C^R'); add_legend(ax, 'northeast');
title('(a) SP saving, r = 0.2'); style_axes(ax);
ax = subplot(1, 2, 2); hold on;
g = 100 * (sav(:, :, [1 3]) - sav(:, :, [2 2]));            % gain over No D2D, points of %
kk = {'lp', 'crowd'};
for j = 1:2, plot_method(ax, ds, mean(g(:, :, j), 1), kk{j}, 11); end
xlabel('Dispersion \delta'); ylabel('Gain over No D2D (points of %)'); add_legend(ax, 'northeast');
title('(b) Value of mobility information'); style_axes(ax);
save_fig(h, 'fig_mobility');
fprintf('exp4: meeting prob %.3f..%.3f; LP %.4f..%.4f; noD2D %.4f..%.4f; crowd %.4f..%.4f\n', mv(1), mv(end), mS(1,1), mS(end,1), mS(1,2), mS(end,2), mS(1,3), mS(end,3));
