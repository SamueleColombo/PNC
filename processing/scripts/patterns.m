function F = patterns(ecgs)
    
    % Create a parser.
    parameter = inputParser;
    
    % Create the ECGs parser.
    checkECGs = @(x) isvector(x) && all(isa(x, 'Signal'));
    addRequired(parameter, 'ecgs', checkECGs);
    
    % Parse the input data.
    parse(parameter, ecgs);
    
    % Initialize the output array.
    F = [];
    
    % Iterate all over the ECGs.
    for i = 1:length(ecgs)
        % Elaborate the signal and find the pattern.
        P = pattern(ecgs(i));
        % Check if some pattern are found.
        if ~isempty(P)
            % Select the features to use in the NN.
            f = features(ecgs(i), 'Method', 2);
            % Update the array of the features.
            F = [F f];
            % Update the features-array to ECG signal.
            ecgs(i).Features = [ecgs(i).Features f];    
        end
        
    end
    
end