classdef Point < dynamicprops
   
    properties
        X                            % The X coordinate.
        Y                            % The Y coordinate.
        Annotations = struct([])     % A structure for annotations.
    end
    
    methods
        function obj = Point(x, y, varargin)
            
            % Create an input parser.
            parameter = inputParser;
            
             % Create the value parser.
            checkX = @(n) isnumeric(n) && isscalar(n);
            addRequired(parameter, 'x', checkX);
            
            % Create the value parser.
            checkY = @(n) isnumeric(n) && isscalar(n);
            addRequired(parameter, 'y', checkY);
            
            % Create the Peak annotation parser.
            defaultPeak = '';
            validPeak = {'P', 'Q', 'R', 'S', 'T'};
            checkPeak = @(n) any(validatestring(n, validPeak));
            addParameter(parameter, 'Peak', defaultPeak, checkPeak);

            % Parse the varagin arguments.
            parse(parameter, x, y, varargin{:});
            
            % Set the object Y.
            obj.X = x;
            
            % Set the object Y.
            obj.Y = y;
            
            % Build the Annotation struct.
            if parameter.Results.Peak ~= ""
                % Set the Peak field.
                obj.Annotations(1).('Peak') = parameter.Results.Peak;
            end
            
            
        end
        
        function set.X(obj, x)
           obj.X = x; 
        end
        
        function set.Y(obj, y)
           obj.Y = y; 
        end
    end
    
    methods (Static)
        function p = Builder(x, y)
            p = Point(x,y);
        end
    end
    
end