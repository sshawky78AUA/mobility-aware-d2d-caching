function add_legend(ax, loc)
%ADD_LEGEND  Legend from the DisplayName of the plotted lines (MATLAB and Octave).
try
    legend(ax, 'Location', loc, 'FontSize', 8);
catch
    legend(ax, 'show'); legend(ax, 'location', loc);
end
end
