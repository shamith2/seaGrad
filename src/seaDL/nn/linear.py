from typing import Optional
from jaxtyping import jaxtyped
from typeguard import typechecked as typechecker

import math

from seaDL import Tensor, Device, DataType, prod
from seaDL.random import uniform

from .base import Parameter, Module


@jaxtyped(typechecker=typechecker)
class Linear(Module):
    def __init__(
            self,
            in_features: int,
            out_features: int,
            bias: bool = True,
            device: Optional[Device] = None,
            dtype: Optional[DataType] = DataType('float32')
    ):
        '''
        A simple linear (affine) transformation: y = xW.T + b
        '''
        super().__init__()

        self.in_features = in_features
        self.out_features = out_features

        scale = math.sqrt(1.0 / in_features)

        self.weight = Parameter(
            uniform(
                low=-scale,
                high=scale,
                size=(out_features, in_features),
                dtype=dtype
            )
        )

        if bias:
            self.bias = Parameter(
                uniform(
                    low=-scale,
                    high=scale,
                    size=(out_features,),
                    dtype=dtype
                )
            )

        else:
            self.bias = None


    def __call__(
            self,
            x: Tensor
    ) -> Tensor:
        '''
        x: shape (*, in_features)
        Return: shape (*, out_features)
        '''
        y = x.matmul(self.weight.transpose())

        if self.bias is not None:
            y = y + self.bias

        return y


    def extra_repr(self) -> str:
        return "in_features: {}, out_features: {}, bias_shape: {}".format(
            self.in_features, self.out_features, self.bias.shape if self.bias is not None else None
        )


@jaxtyped(typechecker=typechecker)
class Flatten(Module):
    def __init__(
            self,
            start_dim: int = 1,
            end_dim: int = -1,
            device: Optional[Device] = None
    ):
        super().__init__()
        
        self.start_dim = start_dim
        self.end_dim = end_dim

    def __call__(
            self,
            x: Tensor
    ) -> Tensor:
        '''
        Flatten out dimensions from start_dim to end_dim, inclusive of both
        '''
        in_shape = x.shape

        self.end_dim = len(in_shape) + self.end_dim if self.end_dim < 0 else self.end_dim

        shape = (in_shape[:self.start_dim] +
                (prod(in_shape[self.start_dim:self.end_dim+1]),) +
                in_shape[self.end_dim+1:])

        return x.reshape(shape)


    def extra_repr(self) -> str:
        return super().extra_repr()

