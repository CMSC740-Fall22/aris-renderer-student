import logging

import torch
from torch import Tensor

from aris.core.scene import Scene
from aris.integrator import Integrator, integrator_registry

logger = logging.getLogger(__name__)


class WhittedIntegrator(Integrator):
    def __init__(self, max_path_length: int, cont_prob: float) -> None:
        super().__init__()
        self.max_path_length = max_path_length
        self.cont_prob = cont_prob

    def render(self, scene: Scene, rays_o: Tensor, rays_d: Tensor) -> Tensor:
        result = torch.zeros_like(rays_d)
        # YOUR TASK: implement the Whitted-style integrator
        return result


integrator_registry.add("whitted", WhittedIntegrator)
