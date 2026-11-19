function Gm = enum_groups(N)
%ENUM_GROUPS  All non-empty subsets of {1..N} as a (2^N-1) x N logical matrix.
idx = (1:2^N-1)';
Gm = false(numel(idx), N);
for n = 1:N
    Gm(:, n) = bitand(idx, 2^(n-1)) > 0;
end
end
