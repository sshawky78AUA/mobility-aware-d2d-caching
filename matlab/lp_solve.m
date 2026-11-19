function [z, fval, ok] = lp_solve(f, A, b, lb, ub, intcon, sense)
%LP_SOLVE  Minimize (sense=+1) or maximize (sense=-1) f'*z s.t. A*z<=b, lb<=z<=ub.
%   Uses linprog / intlinprog (MATLAB Optimization Toolbox) when available,
%   otherwise GLPK (GNU Octave). intcon lists integer variables (binary when
%   their bounds are [0,1]).
if nargin < 6, intcon = []; end
if nargin < 7, sense = 1; end
f = f(:); lb = lb(:); ub = ub(:); b = b(:);
fs = sense * f;
haveMatlab = exist('linprog', 'file') == 2 && exist('OCTAVE_VERSION', 'builtin') == 0;
if haveMatlab
    if isempty(intcon)
        opts = optimoptions('linprog', 'Display', 'none');
        [z, fv, flag] = linprog(fs, A, b, [], [], lb, ub, opts);
    else
        opts = optimoptions('intlinprog', 'Display', 'none');
        [z, fv, flag] = intlinprog(fs, intcon, A, b, [], [], lb, ub, [], opts);
    end
    ok = flag > 0;
else
    nv = numel(f);
    ctype = repmat('U', 1, size(A, 1));
    vtype = repmat('C', 1, nv); vtype(intcon) = 'I';
    ubg = ub; ubg(isinf(ubg)) = 1e12;   % glpk needs finite bounds
    param.msglev = 0;
    [z, fv, status] = glpk(fs, sparse(A), b, lb, ubg, ctype, vtype, 1, param);
    ok = (status == 0 || status == 5 || status == 2);
end
if ~ok || isempty(z), z = nan(numel(f), 1); fval = nan; return; end
fval = sense * fv;
end
