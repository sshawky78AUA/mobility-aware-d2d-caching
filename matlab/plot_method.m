function h = plot_method(ax, x, y, key, nmk)
%PLOT_METHOD  Line in the method's style with about nmk evenly spaced markers.
if nargin < 5, nmk = 8; end
st = method_style(key); x = x(:); y = y(:);
h = plot(ax, x, y, 'LineStyle', st.ls, 'Color', st.c, 'LineWidth', 1.5);
idx = unique(round(linspace(1, numel(x), min(nmk, numel(x)))));
hold(ax, 'on');
plot(ax, x(idx), y(idx), 'LineStyle', 'none', 'Marker', st.mk, 'Color', st.c, ...
     'MarkerFaceColor', 'w', 'MarkerSize', 5, 'HandleVisibility', 'off');
% legend entry with marker
set(h, 'Marker', 'none'); h2 = plot(ax, nan, nan, 'LineStyle', st.ls, 'Color', st.c, 'LineWidth', 1.5, ...
     'Marker', st.mk, 'MarkerFaceColor', 'w', 'MarkerSize', 5, 'DisplayName', st.name);
set(h, 'HandleVisibility', 'off'); h = h2;
end
