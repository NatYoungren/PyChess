import os
import json
import numpy as np
from pathlib import Path


class NpEncoder(json.JSONEncoder):
    """Encoder to translate numpy dtypes into default python data types,
        json.dump cannot handle np types by default.

    Args:
        json ( - ): ignore, hand this directly to json.dump as cls kwarg. (e.g. json.dump(data, f, cls=NpEncoder))
    """
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.bool_):
            return bool(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()

        return super(NpEncoder, self).default(obj)
    
    
def write_json(json_filename: str, data: dict):
    Path(json_filename).parent.mkdir(parents=True, exist_ok=True)  # Ensure directory exists
    with open(os.path.join(json_filename), 'w') as f:
        json.dump(data, f, cls=NpEncoder)

def read_json(json_filename):
    with open(json_filename) as f:
        return json.load(f)

def read_state_json(json_filename: str) -> dict:
    """
    Read a JSON file and return its contents as a dictionary.
    """
    with open(json_filename, 'r') as f:
        data = json.load(f)
    
    # Convert leadership_pts keys to float and values to int
    # TODO: Just use tuples of (loyalty, pts), by turn_order
    fixed_leadership_pts_data = {}
    for k, v in data.get('leadership_pts', {}).items():
        fixed_leadership_pts_data[float(k)] = int(v)
    data['leadership_pts'] = fixed_leadership_pts_data
    
    # Convert 2D lists to numpy arrays
    data['tiles'] = np.array(data['tiles'], dtype=np.int32)  # Convert tiles to numpy array
    data['pieces'] = np.array(data['pieces'], dtype=np.int32)  # Convert pieces to numpy array
    data['piece_loyalties'] = np.array(data['piece_loyalties'], dtype=np.float32)  # Convert loyalties to numpy array
    return data
