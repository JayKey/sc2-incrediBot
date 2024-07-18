from sc2.bot_ai import BotAI
from sc2.ids.unit_typeid import UnitTypeId
import random

class CameraManager:
    def __init__(self, bot: BotAI):
        self.bot = bot
        self.unit_to_follow = None
        self.follow_duration = 50  # Number of game loops to follow the same unit
        self.follow_counter = 0

    async def follow_unit_with_camera(self, unit_to_follow):
        if unit_to_follow:
            await self.bot._client.move_camera(unit_to_follow.position)

    def select_unit_to_follow(self, units):
        # Select a non-worker unit closer to the enemy
        enemy_units = self.bot.enemy_units
        if enemy_units.exists:
            closest_enemy = enemy_units.closest_to(self.bot.start_location)
            # Filter out worker units (Probes)
            non_worker_units = units.filter(lambda unit: unit.type_id not in {UnitTypeId.PROBE})
            if non_worker_units.exists:
                self.unit_to_follow = non_worker_units.closest_to(closest_enemy)
            else:
                self.unit_to_follow = random.choice(units)
        else:
            non_worker_units = units.filter(lambda unit: unit.type_id not in {UnitTypeId.PROBE})
            if non_worker_units.exists:
                self.unit_to_follow = random.choice(non_worker_units)
            else:
                self.unit_to_follow = random.choice(units)

    async def manage_camera(self):
        if self.follow_counter <= 0:
            # Select a new unit to follow
            self.select_unit_to_follow(self.bot.units)
            self.follow_counter = self.follow_duration

        await self.follow_unit_with_camera(self.unit_to_follow)
        self.follow_counter -= 1
