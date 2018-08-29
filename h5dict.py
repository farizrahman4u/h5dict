import numpy as np

try:
    import h5py
    HDF5_OBJECT_HEADER_LIMIT = 64512
except ImportError:
    h5py = None


class H5Dict(object):

    def __init__(self, path, mode='a'):
        if isinstance(path, h5py.Group):
            self.group = path
            self._is_file = False
        elif type(path) is str:
            self.group = h5py.File(path)
            self._is_file = True
        else:
            raise Exception('Required Group or str. Received {}.'.format(type(path)))

    def __setitem__(self, attr, val):
        if isinstance(val, np.ndarray):
            dataset = self.group.create_dataset(attr, val.shape, dtype=val.dtype)
            if not val.shape:
                # scalar
                dataset[()] = val
            else:
                dataset[:] = val
        else:
            self.group.attrs[attr] = val

    def __getitem__(self, attr):
        if attr in self.group.attrs:
            val = self.group.attrs[attr]
        elif attr in self.group:
            val = self.group[attr]
            if isinstance(val, h5py.Dataset):
                val = np.asarray(val)
            else:
                val = H5Dict(val)
        else:
            val = H5Dict(self.group.create_group(attr))
        return val

    def __len__(self):
        return len(self.group)

    def __iter__(self):
        return iter(list(self.group))

    def iter(self):
        return list(self.group)

    def __getattr__(self, attr):

        def wrapper(f):
            def h5wrapper(*args, **kwargs):
                out = f(*args, **kwargs)
                if isinstance(out, h5py.Group):
                    return H5Dict(out)
                else:
                    return out
            return h5wrapper

        return wrapper(getattr(self.group, attr))

    def close(self):
        if self._is_file:
            self.group.close()

    def update(self, *args):
        raise NotImplementedError


h5dict = H5Dict
