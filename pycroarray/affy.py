import ConfigParser
import gzip
import struct

import numpy as np
import numpy.ma as ma

class CELFile(object) :

    def __init__(self,f) :

        if isinstance(f,str) :
            _f = open(f,'rb')

            magic = struct.unpack('BB',_f.read(2))
            if magic == (0x1f,0x8b) :
                f = gzip.open(f)
            else :
                _f.seek(0)
                f = _f

        magic = struct.unpack('BBxx',f.read(4))
        if magic != (0x40,0x00) :
            raise Exception('invalid CEL file, did not find \\x40 \\x00 as first two words, found %s %s instead, aborting'%(hex(magic[0]),hex(magic[1])))

        version, num_cols, num_rows, num_cells, header_len = struct.unpack_from('iiiii',f.read(4*5))
        header = f.read(header_len)

        alg_name_len = struct.unpack_from('i',f.read(4))[0]
        alg_name = f.read(alg_name_len)

        alg_param_len = struct.unpack_from('i',f.read(4))[0]
        alg_params = f.read(alg_param_len)

        cell_margin, num_outliers, num_masked, num_subgrids = struct.unpack_from('iIIi',f.read(4*4))

        cell_data = ma.zeros((num_rows,num_cols,3))
        cell_data_struct = struct.Struct('ffh')
        for i in range(num_rows) :
            # doing this row by row is WAY faster than assigning one element at
            # a time to the numpy array
            whole_row = []
            for j in range(num_cols) :
                intensity, stdev, pixels = cell_data_struct.unpack_from(f.read(4*2+2))
                whole_row.append((intensity,stdev,pixels))
            cell_data[i,:,:] = whole_row

        mask = np.zeros((num_rows,num_cols))
        for i in range(num_masked) :
            masked_i, masked_j = struct.unpack_from('hh',f.read(2*2))
            mask[masked_i,masked_j] = 1

        outliers = np.zeros((num_rows,num_cols))
        for i in range(num_outliers) :
            outlier_i, outlier_j = struct.unpack_from('hh',f.read(2*2))
            outliers[outlier_i,outlier_j] = 1

        self.mask = mask == 1
        self.outliers = outliers == 1

        self.cell_data = cell_data

        self.intensities = cell_data[:,:,0]
        #self.intensities.mask = mask | outliers

        self.stdevs = cell_data[:,:,1]
        #self.stdevs.mask = mask | outliers


#TODO - implement CDFFile class

class AffyArray(object) :

    def __init__(self,cdf_fn,cel_fn) :
        #TODO finish implementing

#TODO implement array-specific classes?
