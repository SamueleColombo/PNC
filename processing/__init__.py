import io
import matlab.engine
import numpy as np
import os

def run(reference = None):
    """

    :param reference:
    :return:
    """

    # Check if MATLAB session is on.
    if matlab.engine.find_matlab():
        # Connect to the existent MATLAB session.
        eng = matlab.engine.connect_matlab()
    else:
        # Start the MATLAB engine.
        eng = matlab.engine.start_matlab()

    # Create MATLAB workspace adding all matlab scripts.
    eng.addpath(eng.genpath(os.path.dirname(__file__), nargout=1), nargout=0)

    # Bind the output stream with MATLAB workspace.
    stdout = io.StringIO()
    # Bind the error stream with MATLAB workspace.
    stderr = io.StringIO()

    if reference:

        if reference.endswith('.csv'):
            # Execute the test file with the selected reference.
            table = eng.main(reference, nargout=1, stdout=stdout, stderr=stderr)
        elif reference.endswith('.mat'):
            # # Load the mat file.
            F = eng.load(reference, 'ecgs', nargout=1, stdout=stdout, stderr=stderr)
            # Convert the Features array.
            table = eng.compact(F['ecgs'], nargout=1, stdout=stdout, stderr=stderr)

    else:
        # Execute the test file.
        table = eng.main(nargout=1, stdout=stdout, stderr=stderr)

    # Transform the MATLAB data into a Python array.
    table = np.asarray([[col for col in row] for row in table], np.float32)

    # Halt the MATLAB engine.
    eng.quit()

    # Return the dataset.
    return table

# execute('C:\\Users\\Samuele\\Documents\\PyCharmProjects\\PNC\\pnc\\test\\PNC-data\\REFERENCE.csv')
# execute('C:\\Users\\Samuele\\Documents\\PyCharmProjects\\PNC\\pnc\\test\\PNC-features\\F.mat')