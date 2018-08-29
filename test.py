from numpy.testing import assert_allclose
from h5dict import H5Dict
import numpy as np
import pytest


def test_attr():
    f = H5Dict('test.h5')
    f['x'] = 'abcd'
    f['y'] = 'efgh'
    f.close()
    f = H5Dict('test.h5')
    assert f['x'] == 'abcd'
    assert f['y'] == 'efgh'


def test_group():
    f = H5Dict('test.h5')
    f.clear()  # clear stuff from previous test
    f['x'] = 'abcd'
    group1 = f['g1']
    group1['x'] = 'efgh'
    f['g2']['x'] = 'xyz'
    f.close()
    f = H5Dict('test.h5')
    assert f['x'] == 'abcd'
    assert f['g1']['x'] == 'efgh'
    assert f['g2']['x'] == 'xyz'


def test_dataset():
    arr1 = np.random.random((32, 16, 10))
    arr2 = np.random.random((10, 12))
    arr3 = np.random.random(10)
    f = H5Dict('test.h5')
    f.clear()  # clear stuff from previous test
    f['arr1'] = arr1
    group1 = f['group1']
    group1['arr2'] = arr2
    f['group1']['group2']['arr3'] = arr3
    f.close()
    f = H5Dict('test.h5')
    assert_allclose(f['arr1'], arr1)
    assert_allclose(f['group1']['arr2'], arr2)
    assert_allclose(f['group1']['group2']['arr3'], arr3)


if __name__ == '__main__':
    pytest.main([__file__])
