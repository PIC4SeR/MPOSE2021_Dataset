import os
from init_vars import *

for i in samples_to_remove:
    if os.path.exists(os.path.join(paths['rgb'], i)):
        os.remove(os.path.join(paths['rgb'], i))
        os.remove(os.path.join(paths['pose'], i))



