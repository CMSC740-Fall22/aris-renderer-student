from abc import ABC, abstractmethod

from torch import Tensor

from aris.core.scene import Scene
from aris.utils.import_utils import import_children
from aris.utils.registry_utils import Registry


class Integrator(ABC):
    @abstractmethod
    def render(self, scene: Scene, rays_o: Tensor, rays_d: Tensor) -> Tensor:
        """Render a batch of rays in the scene.

        rays_o: (N, 3) ray origins
        rays_d: (N, 3) ray directions (not normalized)
        """
        raise NotImplementedError()

    def on_render_ended(self) -> None:
        """Called when render completes.

        You can print some statistics, for example.
        """

integrator_registry = Registry("integrator", Integrator)
import_children(__file__, __name__)
