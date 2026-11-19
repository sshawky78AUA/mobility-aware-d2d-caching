function save_fig(h, name)
%SAVE_FIG  Write a figure as EPS, PDF (MATLAB only) and PNG.
d = fullfile(fileparts(mfilename('fullpath')), '..', 'figs');
if ~exist(d, 'dir'), mkdir(d); end
set(h, 'PaperPositionMode', 'auto');
print(h, fullfile(d, [name '.eps']), '-depsc2');
print(h, fullfile(d, [name '.png']), '-dpng', '-r150');
if exist('OCTAVE_VERSION', 'builtin') == 0   % MATLAB: vector PDF for pdflatex
    set(h, 'PaperUnits', 'points', 'PaperSize', h.Position(3:4));
    print(h, fullfile(d, [name '.pdf']), '-dpdf');
end
end
