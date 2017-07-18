function P = pattern(ecg)
    
    % The array of the pattern found in the ECG signal.
    P = struct();
    
    % Perform the regularity filter on the signal and get a new one.
    %S = Signal(regularity(ecg), ecg.Target, ecg.Name);
    S = ecg;
    
    % Get the R-peaks using this method.
    % p = peaks(S);
    
    % Get the R-peaks using the PT method.
    [xq, xr, xs] = pan_tompkin_qrs(S.Values, 300, false);
    
    % Get the y-coordinate of the Q-peaks.
    yq = S.Values(xq);
    % Get the y-coordinate of the R-peaks.
    yr = S.Values(xr);
    % Get the y-coordinate of the S-peaks.
    ys = S.Values(xs);
    
    % Save this data into the signal.
    % TODO: Are you sure to waste memory in that way?
    Q = arrayfun(@(x,y) Point(x,y, 'Peak','Q'), xq, yq, 'UniformOutput', false);
    R = arrayfun(@(x,y) Point(x,y, 'Peak','R'), xr, yr, 'UniformOutput', false);
    S = arrayfun(@(x,y) Point(x,y, 'Peak','S'), xs, ys, 'UniformOutput', false);
    ecg.Points = [Q{:} R{:} S{:}];
    
    % Get the QRS-complex using another method.
    P.('Q') = xq;
    P.('R') = xr;
    P.('S') = xs;
   

end