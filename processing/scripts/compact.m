function T = compact(E)

    % Create the parser.
    p = inputParser;

    % Create a validator for the F argument.
    checkSignal = @(x) isvector(x) && all(isa(x, 'Signal'));
    addRequired(p, 'E', checkSignal);

    % Validate the input data.
    parse(p, E);
    
    % Declare the output array.
    T = [];
    
    for i = 1:length(E)
        % Get the features array.
        F = E(i).Features;
        % TODO: Not all the file are been processed.
        if ~isempty(F)
            % Get the values.
            G = [F.Values];
            % Calculate the width.
            width = numel(F(1).Values);
            % Calculate the heigth.
            height = numel(E.Features);
            % Reshape the array into a matrix.
            H = reshape([G.Value], width, height)';
            % Compatibility problem between Python and MATLAB: they cannot
            % string string-arrays. So, the name of the ECG record will be 
            % converted into a integer counter.
            
            % Attach the name column.
            % H = [H, repmat(E(i).Name, size(H, 1), ];
                        
            % Save the current line if it doesn't contain NaN.
            if nnz(isnan(double(H(:,2:end)))) == 0
                T = [T, H];
            end
        end
    end
    
    


end