function [wm] = wmean(values)
    % Discretize the data splitting them in bins.
    hg = histogram(values);
    % Medium value of the each bin.
    mv = hg.BinEdges(1:end-1) + hg.BinWidth / 2;
    % Calculate the weighted mean from values and weights.
    wm = sum(hg.Values .* mv) / sum(hg.Values);
end