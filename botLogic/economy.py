from sc2.ids.unit_typeid import UnitTypeId

class EconomyManager:
    def __init__(self, bot):
        self.bot = bot

    async def manage_economy(self):
        await self.bot.distribute_workers()

        if self.bot.townhalls:
            nexus = self.bot.townhalls.random

            # Train probes if the nexus is not fully saturated
            if (nexus.assigned_harvesters < nexus.ideal_harvesters
                    and nexus.is_idle
                    and self.bot.can_afford(UnitTypeId.PROBE)):
                nexus.train(UnitTypeId.PROBE)

            # Build gas extractors if we have a gateway and don't have enough
            if (self.bot.structures(UnitTypeId.GATEWAY).ready.exists
                    and self.bot.already_pending(UnitTypeId.ASSIMILATOR) == 0):
                for geyser in self.bot.vespene_geyser.closer_than(10, nexus):
                    if await self.bot.can_place(UnitTypeId.ASSIMILATOR, geyser.position):
                        worker = self.bot.select_build_worker(geyser.position)
                        if worker is not None and self.bot.can_afford(UnitTypeId.ASSIMILATOR):
                            await self.bot.build(UnitTypeId.ASSIMILATOR, geyser)
                            break
