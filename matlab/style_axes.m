function style_axes(ax)
set(ax, 'FontSize', 10, 'Box', 'on', 'LineWidth', 0.8); grid(ax, 'on');
try, set(ax, 'GridAlpha', 0.25); catch, end     % not available in Octave
end
