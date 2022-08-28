from abc import ABC, abstractmethod
from dataclasses import dataclass

from torch import Tensor

from aris.geometry import Geometry
from aris.utils.import_utils import import_children
from aris.utils.registry_utils import Registry


@dataclass
class EmitterQuery:
    # (N, 3) points on the emitter
    points: Tensor
    # (N, 3) normals of above points
    normals: Tensor
    # (N,) pdf of the emitter sampling these points
    pdf: Tensor = None
    # (N, 3) points to be lit
    targets: Tensor = None
    # (N, 3) computed Le
    le: Tensor = None
    # (N,) where Le is not zero
    mask: Tensor = None
    # (N, 3) direction (normalized) from targets to points
    d_target_point: Tensor = None


class Emitter(ABC):
    @abstractmethod
    def sample(self, n_samples: int, device: str) -> EmitterQuery:
        raise NotImplementedError()

    @abstractmethod
    def pos_pdf(self, query: EmitterQuery) -> EmitterQuery:
        raise NotImplementedError()

    @abstractmethod
    def le(self, query: EmitterQuery, geometry: Geometry) -> EmitterQuery:
        raise NotImplementedError()


emitter_registry = Registry("emitter", Emitter)
import_children(__file__, __name__)
