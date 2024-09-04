import torch
import torch.nn.functional as F
import numpy as np
import mlx.core as mx
import pytest

import seaML.nn as nn


@pytest.fixture
def pytest_configure():
    pytest.device = mx.gpu
    pytest.n_tests = 10


def test_pad1d(pytest_configure):
    '''
    Should work with one channel of width 4
    '''
    x = mx.arange(4, dtype=mx.float32).reshape((1, 1, 4))

    actual = nn.functional.pad1d(x, 1, 3, -2.0, pytest.device)
    expected = mx.array([[[-2.0, 0.0, 1.0, 2.0, 3.0, -2.0, -2.0, -2.0]]])
    assert mx.allclose(actual, expected).all()

    actual = nn.functional.pad1d(x, 1, 0, -2.0, pytest.device)
    expected = mx.array([[[-2.0, 0.0, 1.0, 2.0, 3.0]]])
    assert mx.allclose(actual, expected).all()


def test_pad1d_multi_channel(pytest_configure):
    '''
    Should work with two channels of width 2
    '''
    x = mx.arange(4, dtype=mx.float32).reshape((1, 2, 2))
    expected = mx.array([[[0.0, 1.0, -3.0, -3.0], [2.0, 3.0, -3.0, -3.0]]])

    actual = nn.functional.pad1d(x, 0, 2, -3.0, pytest.device)
    assert mx.allclose(actual, expected).all()


def test_pad2d(pytest_configure):
    '''
    Should work with one channel of 2x2
    '''
    x = mx.arange(4, dtype=mx.float32).reshape((1, 1, 2, 2))
    expected = mx.array([[[
        [0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [2.0, 3.0, 0.0],
        [0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0]
    ]]])


    actual = nn.functional.pad2d(x, 2, 3, 0, 1, 0.0, pytest.device)
    assert mx.allclose(actual, expected).all()


def test_pad2d_multi_channel(pytest_configure):
    '''
    Should work with two channels of 2x1
    '''
    x = mx.arange(4, dtype=mx.float32).reshape((1, 2, 2, 1))
    expected = mx.array([[[[-1.0, 0.0], [-1.0, 1.0], [-1.0, -1.0]], [[-1.0, 2.0], [-1.0, 3.0], [-1.0, -1.0]]]])
    
    actual = nn.functional.pad2d(x, 0, 1, 1, 0, -1.0, pytest.device)
    assert mx.allclose(actual, expected).all()


def test_conv1d(pytest_configure):
    for _ in range(pytest.n_tests):
        b = mx.random.randint(1, 10)
        h = mx.random.randint(10, 300)
        ci = mx.random.randint(1, 20)
        co = mx.random.randint(1, 20)
        stride = mx.random.randint(1, 5)
        padding = mx.random.randint(0, 5)
        kernel_size = mx.random.randint(1, 10)

        x = mx.random.normal(shape=(b.item(), ci.item(), h.item()))
        x_torch = torch.from_numpy(np.array(x))

        weights = mx.random.normal(shape=(co.item(), ci.item(), kernel_size.item()))
        weights_torch = torch.from_numpy(np.array(weights))

        my_output = nn.functional.conv1d(
            x,
            weights,
            stride=stride.item(),
            padding=padding.item(),
            device=pytest.device
        )

        my_output_torch = torch.from_numpy(np.array(my_output))

        torch_output = F.conv1d(x_torch, weights_torch, stride=stride.item(), padding=padding.item())

        torch.testing.assert_close(my_output_torch, torch_output, atol=1e-4, rtol=1e-5)


def test_conv2d(pytest_configure):
    for _ in range(pytest.n_tests):
        b = mx.random.randint(1, 10)
        h = mx.random.randint(10, 300)
        w = mx.random.randint(10, 300)
        ci = mx.random.randint(1, 20)
        co = mx.random.randint(1, 20)
        stride = tuple(mx.random.randint(1, 5, shape=(2,)).tolist())
        padding = tuple(mx.random.randint(0, 5, shape=(2,)).tolist())
        kernel_size = tuple(mx.random.randint(1, 10, shape=(2,)).tolist())
        
        x = mx.random.normal(shape=(b.item(), ci.item(), h.item(), w.item()), dtype=mx.float32)
        x_torch = torch.from_numpy(np.array(x))

        weights = mx.random.normal(shape=(co.item(), ci.item(), *kernel_size), dtype=mx.float32)
        weights_torch = torch.from_numpy(np.array(weights))

        my_output = nn.functional.conv2d(
            x,
            weights,
            stride=stride,
            padding=padding,
            device=pytest.device
        )

        my_output_torch = torch.from_numpy(np.array(my_output))

        torch_output = torch.conv2d(x_torch, weights_torch, stride=stride, padding=padding)

        torch.testing.assert_close(my_output_torch, torch_output, atol=1e-4, rtol=1e-5)

