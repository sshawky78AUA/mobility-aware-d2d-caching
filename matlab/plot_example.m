function plot_example(matfile)
%PLOT_EXAMPLE  Fig. 3 (worked example) from the data saved by exp0_example.
if nargin < 1, matfile = fullfile('..', 'figs', 'exp0.mat'); end
d = load(matfile); cu = {[0.30 0.45 0.69], [0.87 0.52 0.32], [0.33 0.66 0.41]};
h = figure('Position', [100 100 1100 330]);
% (a) centralized: stacked placement
ax = subplot(1, 3, 1); hold on; stack_steps([d.rs, 1], [d.Xc, d.Xc(:, end)], cu);
xline_dash([min(d.tau), max(d.sn)]); xlim([0 1]); ylim([0 3.4]); set(gca, 'YTick', 0:0.5:3);
set(ax, 'XTick', [0 min(d.tau) 0.5 max(d.sn) 1], 'XTickLabel', {'0', 'r_1', '0.5', 'r_N', '1'});
xlabel('Reward r'); ylabel('Copies cached, \Sigma_n x_n / S'); title('(a) Centralized: SP decides');
legend({'user 1', 'user 2', 'user 3'}, 'Location', 'northeast'); style_axes(ax);
% (b) decentralized (fair NE) on the same reward axis, r = y_o - r'
ax = subplot(1, 3, 2); hold on;
xr = fliplr(d.yo - d.rps); Xd = fliplr(d.Xf); mu = fliplr(d.multi); pf = fliplr(~d.propOK);
xr = [0, xr]; Xd = [zeros(size(Xd, 1), 1), Xd]; mu = [false, mu]; pf = [false, pf];   % no caching below the data range
stack_steps(xr, Xd, cu);
strip(xr, mu, 3.12, 3.24, [0.6 0.6 0.6]); strip(xr, pf, 3.27, 3.39, [0.77 0.31 0.32]);
xline_dash([d.yo - max(d.phat), d.yo - min(d.tau)]); xlim([0 1]); ylim([0 3.4]); set(gca, 'YTick', 0:0.5:3);
set(ax, 'XTick', [0, d.yo - max(d.phat), d.yo - min(d.tau)], 'XTickLabel', {'$0$', '$1-\hat{p}_1$', '$1-\tilde{p}_3$'});
try, set(ax, 'TickLabelInterpreter', 'latex'); catch, end
xlabel('Reward r (users pay r'' = 1 - r)'); ylabel('Copies cached, \Sigma_n x_n / S'); title('(b) Decentralized: fair NE'); style_axes(ax);
% (c) SP cost: regimes, gap, and the solution of (P2)
ax = subplot(1, 3, 3); hold on;
r_lo = d.yo - max(d.phat); r_hi = d.rr(find(d.rr > r_lo & d.CP(2, :) > 1 + 1e-6, 1));
gap = d.CP(2, :) > d.CP(1, :) + 1e-9;
fill_between(d.rr, d.CP(1, :), d.CP(2, :), gap, [0.77 0.31 0.32]);
plot(d.rr, d.CP(1, :), 'k-', 'LineWidth', 1.6); plot(d.rr, d.CP(2, :), '-', 'Color', cu{1}, 'LineWidth', 1.6);
[v, k] = min(d.CP(2, :)); plot(d.rr(k), v, 'kp', 'MarkerFaceColor', 'y', 'MarkerSize', 11);
plot([0 1], [1 1], ':', 'Color', [0.5 0.5 0.5], 'HandleVisibility', 'off');
for x = [r_lo r_hi], plot([x x], [0 2.6], '--', 'Color', [0.3 0.3 0.3], 'HandleVisibility', 'off'); end
text(r_lo / 2, 2.35, {'users do', 'not cache'}, 'HorizontalAlignment', 'center', 'FontSize', 7);
text((r_lo + r_hi) / 2, 2.35, {'near', 'optimal'}, 'HorizontalAlignment', 'center', 'FontSize', 7);
text((r_hi + 1) / 2, 0.5, {'users', 'over-cache'}, 'HorizontalAlignment', 'center', 'FontSize', 7);
ylim([0 2.6]); xlim([0 1]); xlabel('Reward r'); ylabel('SP cost C^P / C^R'); title('(c) Resulting SP cost');
legend({'cost of decentralization', 'centralized', 'decentralized (fair NE)', 'best reward, (P2)'}, 'Location', 'west'); style_axes(ax);
save_fig(h, 'fig_example');
end

function stack_steps(x, X, cu)
base = zeros(1, numel(x)); xs = [x; x]; xs = xs(:)'; xs = xs(2:end);
for n = 1:size(X, 1)
    top = base + X(n, :);
    yb = [base; base]; yb = yb(:)'; yb = yb(1:end-1); yt = [top; top]; yt = yt(:)'; yt = yt(1:end-1);
    fill([xs, fliplr(xs)], [yt, fliplr(yb)], cu{n}, 'EdgeColor', 'none', 'FaceAlpha', 0.85);
    base = top;
end
stairs(x, base, 'k-', 'LineWidth', 1.0, 'HandleVisibility', 'off');
end

function strip(x, mask, y0, y1, c)
m = diff([0, mask(:)', 0]); st = find(m == 1); en = find(m == -1) - 1;
for k = 1:numel(st)
    if en(k) > st(k)
        x1 = x(min(en(k) + 1, numel(x)));
        fill([x(st(k)) x1 x1 x(st(k))], [y0 y0 y1 y1], c, 'EdgeColor', 'none', 'HandleVisibility', 'off');
    end
end
end

function xline_dash(v)
for k = 1:numel(v), plot([v(k) v(k)], [0 3.4], '--', 'Color', [0.3 0.3 0.3], 'HandleVisibility', 'off'); end
end

function fill_between(x, y0, y1, mask, c)
m = diff([0, mask(:)', 0]); st = find(m == 1); en = find(m == -1) - 1; first = true;
for k = 1:numel(st)
    idx = st(k):en(k);
    if numel(idx) < 2, continue; end
    hf = fill([x(idx), fliplr(x(idx))], [y0(idx), fliplr(y1(idx))], c, 'FaceAlpha', 0.18, 'EdgeColor', 'none');
    if ~first, set(hf, 'HandleVisibility', 'off'); end
    first = false;
end
end
