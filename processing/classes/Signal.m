classdef Signal < dynamicprops
   
    properties
        Name = ''                   % The record name.
        Values                      % The ECG values.
        Points = Point.empty()      % The Point-array.
        Target                      % The target class.
        Features = Features.empty() % The Features-array.
    end
    
    methods 
        function obj = Signal(values, target, varargin)
            
            % Create an input parser.
            parameter = inputParser;
            
            % Create the Values parser.
            checkValues = @(x) isvector(x) && isnumeric(x);
            addRequired(parameter, 'Values', checkValues);
            
            % Create the Target parser.
            checkTarget = @(x) isnumeric(x) && isscalar(x) && (x >= 0);
            addRequired(parameter, 'Target', checkTarget);
            
            % Create the Name parser.
            defaultName = '';
            checkName = @(x) isstring(x);
            addOptional(parameter, 'Name', defaultName, checkName);
            
            % Create the Points parser.
            defaultPoints = Point.empty();
            checkPoints = @(x) isvector(x) && all(isa(x, 'Point'));
            addParameter(parameter, 'Points', defaultPoints, checkPoints);
            
            % Create the Points parser.
            defaultFeatures = Features.empty();
            checkFeatures = @(x) isvector(x) && all(isa(x, 'Features'));
            addParameter(parameter, 'Features', defaultFeatures, checkFeatures);
            
            % Parse the varagin arguments.
            parse(parameter, values, target, varargin{:});
            
            % Set the Values array.
            obj.Values = values;
             
            % Check if the Points parameter is present.
            if ~isequal(parameter.Results.Points, Point.empty())
                % Set the Points property.
                obj.Points = parameter.Results.Points;
            end
            
           % Set the Name property.
           obj.Name = parameter.Results.Name;
            
%             % Set th object values.
%             if any(isnumeric(values))
%                % Create the a cell array.
%                cells = arrayfun(@(k, v) Point(k, v), 1:length(values), values, 'UniformOutput', false);
%                % Conver the cell array into Point one.
%                obj.Values = [cells{1,:}];
%             end
            
            
            % Set the object Target.
            obj.Target = target;
            
        end
        
        function B = Filter(obj, varargin)
            
            % Create an input parser.
            parameter = inputParser;
            
            % Create the Peak Filter parser.
            defaultPeak = '';
            validPeak = {'P', 'Q', 'R', 'S', 'T'};
            checkPeak = @(x) any(validatestring(x, validPeak));
            addParameter(parameter, 'Peak', defaultPeak, checkPeak);
            
            % Parse the varagin arguments.
            parse(parameter, varargin{:});
            
            % The logical array of the selected point.
            B = obj.Points;
            
            if parameter.Results.Peak ~= ""
                % Get all the indexes that are related to the selected
                % peak.
               A = arrayfun(@(x) x.Peak == parameter.Results.Peak, [B.Annotations]);
               B = B(A);
            end
            
        end
    end
    
end