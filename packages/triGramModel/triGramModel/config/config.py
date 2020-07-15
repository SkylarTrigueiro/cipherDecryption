import triGramModel
import pathlib
import os


PACKAGE_ROOT = pathlib.Path(triGramModel.__file__).resolve().parent
TRAINED_MODEL_DIR = PACKAGE_ROOT / 'trained_models'
DATA_DIR = PACKAGE_ROOT / 'datasets'

# data
TRAIN_DATA = 'moby_dick.txt'
TEST_DATA = 'test.txt'

# Cipher Maps
TRUE_MAP_NAME = 'true_map'
BEST_MAP_NAME = 'best_map'


# Parameters
CREATE_CIPHER = True
ITERS = 1000

with open(os.path.join(PACKAGE_ROOT, 'VERSION')) as version_file:
    _version = version_file.read().strip()

TRUE_MAP_FILE_NAME = f'{TRUE_MAP_NAME}_{_version}.pkl'
BEST_MAP_FILE_NAME = f'{BEST_MAP_NAME}_{_version}.pkl'
