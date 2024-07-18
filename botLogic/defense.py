from sc2.ids.unit_typeid import UnitTypeId
import random

class DefenseManager:
    def __init__(self, bot):
        self.bot = bot

    async def manage_defense(self):
        if self.bot.townhalls:
            nexus = self.bot.townhalls.random

            if not self.bot.structures(UnitTypeId.PYLON) and self.bot.already_pending(UnitTypeId.PYLON) == 0:
                if self.bot.can_afford(UnitTypeId.PYLON):
                    await self.bot.build(UnitTypeId.PYLON, near=nexus)

            elif self.bot.structures(UnitTypeId.PYLON).amount < 5:
                if self.bot.can_afford(UnitTypeId.PYLON):
                    target_pylon = self.bot.structures(UnitTypeId.PYLON).closest_to(self.bot.enemy_start_locations[0])
                    pos = target_pylon.position.towards(self.bot.enemy_start_locations[0], random.randrange(8, 15))
                    await self.bot.build(UnitTypeId.PYLON, near=pos)

            elif not self.bot.structures(UnitTypeId.FORGE):
                if self.bot.can_afford(UnitTypeId.FORGE):
                    await self.bot.build(UnitTypeId.FORGE, near=self.bot.structures(UnitTypeId.PYLON).closest_to(nexus))

            elif self.bot.structures(UnitTypeId.FORGE).ready and self.bot.structures(UnitTypeId.PHOTONCANNON).amount < 3:
                if self.bot.can_afford(UnitTypeId.PHOTONCANNON):
                    await self.bot.build(UnitTypeId.PHOTONCANNON, near=nexus)
