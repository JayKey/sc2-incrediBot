from sc2.ids.unit_typeid import UnitTypeId

class ProductionManager:
    def __init__(self, bot):
        self.bot = bot

    async def manage_production(self):
        if not self.bot.townhalls:
            if self.bot.can_afford(UnitTypeId.NEXUS):
                await self.bot.expand_now()

        if self.bot.townhalls:
            nexus = self.bot.townhalls.random

            # Build Pylon if we don't have any or if supply is low
            if not self.bot.structures(UnitTypeId.PYLON) or self.bot.supply_left < 5:
                if self.bot.can_afford(UnitTypeId.PYLON):
                    await self.bot.build(UnitTypeId.PYLON, near=nexus)

            # Build Gateway if we don't have any and we have a Pylon
            if not self.bot.structures(UnitTypeId.GATEWAY) and self.bot.structures(UnitTypeId.PYLON):
                if self.bot.can_afford(UnitTypeId.GATEWAY):
                    await self.bot.build(UnitTypeId.GATEWAY, near=self.bot.structures(UnitTypeId.PYLON).closest_to(nexus))

            # Build Cybernetics Core if we have a Gateway but no Cybernetics Core
            if self.bot.structures(UnitTypeId.GATEWAY).ready and not self.bot.structures(UnitTypeId.CYBERNETICSCORE):
                if self.bot.can_afford(UnitTypeId.CYBERNETICSCORE):
                    await self.bot.build(UnitTypeId.CYBERNETICSCORE, near=self.bot.structures(UnitTypeId.PYLON).closest_to(nexus))

            # Build additional Gateways after we have a Cybernetics Core
            if self.bot.structures(UnitTypeId.CYBERNETICSCORE).ready and self.bot.structures(UnitTypeId.GATEWAY).amount < 6:
                if self.bot.can_afford(UnitTypeId.GATEWAY):
                    await self.bot.build(UnitTypeId.GATEWAY, near=self.bot.structures(UnitTypeId.PYLON).closest_to(nexus))
