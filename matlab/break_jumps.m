function [xb, yb] = break_jumps(x, y, tol)
%BREAK_JUMPS  Insert NaN where y jumps by more than tol, so that plot()
%   shows a discontinuity instead of a vertical line.
if nargin < 3, tol = 0.02; end
j = find(abs(diff(y)) > tol) + 1; xb = x; yb = y;
for k = numel(j):-1:1
    xb = [xb(1:j(k)-1), NaN, xb(j(k):end)]; yb = [yb(1:j(k)-1), NaN, yb(j(k):end)];
end
end
