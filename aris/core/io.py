from omegaconf import OmegaConf

from aris.brdf import brdf_registry
from aris.camera import camera_registry
from aris.config.object_config import ObjectConfig
from aris.config.scene_config import SceneConfig
from aris.core.scene import Scene
from aris.emitter import emitter_registry
from aris.environment import environment_registry
from aris.geometry import geometry_registry
from aris.integrator import Integrator, integrator_registry


def build_scene(config: SceneConfig) -> Scene:
    camera_config = OmegaConf.to_container(config.camera.config)
    camera_config.update({
        "width": config.width,
        "height": config.height,
    })
    camera = camera_registry.build(config.camera.name, camera_config)
    if config.environment.name == "none":
        environment = None
    else:
        environment = environment_registry.build(config.environment.name, config.environment.config)
    brdf = [
        brdf_registry.build(cfg.name, cfg.config) for cfg in config.brdf
    ]

    geometry = geometry_registry.build(config.geometry.name, config.geometry.config)
    assert len(brdf) == len(geometry), \
        f"The geometry has {len(geometry)} primitives, but found {len(brdf)} BRDF config(s)"

    emitters = []
    for i, cfg in enumerate(config.emitters):
        emitter_cfg = OmegaConf.to_container(cfg.config)
        if "geometry" in emitter_cfg:
            emitter_cfg["geometry"] = geometry
        if "idx" in emitter_cfg:
            emitter_cfg["idx"] = i
        emitters.append(emitter_registry.build(cfg.name, emitter_cfg))

    return Scene(
        geometry,
        brdf,
        camera,
        environment,
        emitters,
    )


def build_integrator(config: ObjectConfig) -> Integrator:
    return integrator_registry.build(config.name, config.config)
