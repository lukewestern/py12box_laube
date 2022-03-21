from pathlib import Path as _pth

_ROOT = _pth(__file__).parents[1]

def get_data(sub_path):
    """Get path to data files

    Parameters
    ----------
    sub_path : str
        path to data files, relative to py12box_agage/data directory

    Returns
    -------
    pathlib.Path
        pathlib Path to data folder/file
    
    """
    
    if sub_path[0] == "/":
        raise Exception("sub-path can't begin with '/'")

    data_path = _ROOT / "data" / sub_path

    return data_path

#import agage_process
#import agage_process_archive
#import agage_data