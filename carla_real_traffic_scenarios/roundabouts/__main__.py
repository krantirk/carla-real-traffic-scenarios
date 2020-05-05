import carla
from libs.carla_real_traffic_scenarios.carla_real_traffic_scenarios.roundabouts import ExitingRoundaboutScenario
from sim2real.carla import DT

def set_birds_eye_view_spectator(
        spectator: carla.Actor, followed_location: carla.Location, above: float
):
    birds_eye_view = carla.Transform(
        carla.Location(x=followed_location.x, y=followed_location.y, z=above),
        carla.Rotation(pitch=-90),
    )
    spectator.set_transform(birds_eye_view)
client = carla.Client("localhost", 2000)
client.set_timeout(3.0)

world = client.get_world()
settings = world.get_settings()
# settings.synchronous_mode = True
# settings.fixed_delta_seconds = DT
# world.apply_settings(settings)

map = world.get_map()
blueprints = world.get_blueprint_library()
bp = blueprints.find("vehicle.audi.a2")
bp.set_attribute("role_name", "hero")
agent_vehicle = world.spawn_actor(bp, map.get_spawn_points()[0])

spectator = world.get_spectator()
scenario = ExitingRoundaboutScenario(world)
scenario.reset(agent_vehicle)
# world.tick()
done = False


try:
    while True:
        result = scenario.step(agent_vehicle)
        if result.done:
            scenario.reset(agent_vehicle)

        # world.tick()
        # set_birds_eye_view_spectator(spectator, scenario.dummy_vehicle.get_location(), above=10)
finally:
    settings = world.get_settings()
    settings.synchronous_mode = False
    settings.fixed_delta_seconds = None
    scenario.close()
    agent_vehicle.destroy()