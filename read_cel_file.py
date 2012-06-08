import sys
from pylab import *

from pycroarray.affy import CELFile

fn = sys.argv[1]
cel = CELFile(fn)

#imshow(cel.intensities)
#imshow(cel.outliers,cmap='binary')
flat_intensities = cel.intensities.flatten()
flat_intensities.sort()
plot(log(flat_intensities))
show()


