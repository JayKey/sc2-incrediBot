from sc2.ids.unit_typeid import UnitTypeId

class AggressionManager:
    def __init__(self, bot):
        self.bot = bot

    async def manage_aggression(self):
        # Basic aggression logic: build offensive units and attack when possible
        if self.bot.units(UnitTypeId.ZEALOT).amount + self.bot.units(UnitTypeId.STALKER).amount > 10:
            for unit in self.bot.units(UnitTypeId.ZEALOT).idle | self.bot.units(UnitTypeId.STALKER).idle:
                unit.attack(self.bot.enemy_start_locations[0])

        # Build Zealots and Stalkers if we have the resources and required structures
        if self.bot.structures(UnitTypeId.GATEWAY).ready.exists:
            if self.bot.can_afford(UnitTypeId.ZEALOT):
                for gw in self.bot.structures(UnitTypeId.GATEWAY).idle:
                    gw.train(UnitTypeId.ZEALOT)
            if self.bot.structures(UnitTypeId.CYBERNETICSCORE).ready.exists and self.bot.can_afford(UnitTypeId.STALKER):
                for gw in self.bot.structures(UnitTypeId.GATEWAY).idle:
                    gw.train(UnitTypeId.STALKER)
