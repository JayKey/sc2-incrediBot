from sc2.ids.unit_typeid import UnitTypeId

class AggressionManager:
    def __init__(self, bot):
        self.bot = bot
        self.unit_queue = []

    async def manage_aggression(self):
        # Check for enemy units and their types
        enemy_units = self.bot.enemy_units
        if enemy_units.exists:
            # Determine the type of enemy units present
            enemy_types = set(unit.type_id for unit in enemy_units)

            # Adjust unit queue based on enemy unit types
            if UnitTypeId.ZERGLING in enemy_types:
                # If enemy has Zerglings, prioritize Stalkers for ranged advantage
                self.adjust_queue([UnitTypeId.STALKER])
            elif UnitTypeId.ROACH in enemy_types:
                # If enemy has Roaches, prioritize Zealots for melee advantage
                self.adjust_queue([UnitTypeId.ZEALOT])
            elif UnitTypeId.HYDRALISK in enemy_types:
                # If enemy has Hydralisks, prioritize Adepts for Disruption Web
                self.adjust_queue([UnitTypeId.ADEPT])
            else:
                # If enemy has other types, use a balanced approach
                self.adjust_queue([UnitTypeId.ZEALOT, UnitTypeId.STALKER, UnitTypeId.ADEPT])

            # Attack enemy units
            for unit in self.bot.units(UnitTypeId.ZEALOT).idle | self.bot.units(UnitTypeId.STALKER).idle | self.bot.units(UnitTypeId.ADEPT).idle:
                if enemy_units.exists:
                    closest_enemy = enemy_units.closest_to(unit)
                    unit.attack(closest_enemy)
        else:
            # If no enemy units are seen, use balanced approach
            self.adjust_queue([UnitTypeId.ZEALOT, UnitTypeId.STALKER, UnitTypeId.ADEPT])
            # If no enemy units are seen, attack the enemy start location
            if self.bot.units(UnitTypeId.ZEALOT).amount + self.bot.units(UnitTypeId.STALKER).amount + self.bot.units(UnitTypeId.ADEPT).amount > 10:
                for unit in self.bot.units(UnitTypeId.ZEALOT).idle | self.bot.units(UnitTypeId.STALKER).idle | self.bot.units(UnitTypeId.ADEPT).idle:
                    unit.attack(self.bot.enemy_start_locations[0])

        # Build units from the queue
        self.build_from_queue()

    def adjust_queue(self, unit_types):
        # Clear the queue and add new unit types
        #self.unit_queue.clear()
        self.unit_queue.extend(unit_types)

    def build_from_queue(self):
        if self.bot.structures(UnitTypeId.GATEWAY).ready.exists and self.unit_queue:
            for gw in self.bot.structures(UnitTypeId.GATEWAY).idle:
                if self.unit_queue:
                    unit_to_train = self.unit_queue[0]
                    if self.bot.can_afford(unit_to_train):
                        gw.train(self.unit_queue.pop(0))
                    else:
                        # Move the unit to the end of the queue if we can't afford it
                        self.unit_queue.append(self.unit_queue.pop(0))

    async def follow_unit_with_camera(self):
        if self.follow_counter <= 0:
            # Select a new unit to follow
            self.select_unit_to_follow()
            self.follow_counter = self.follow_duration

        if self.unit_to_follow:
            print(self.unit_to_follow)
            print(self.unit_to_follow.position)
            await self.bot._client.move_camera(self.unit_to_follow.position)
        else:
            self.unit_to_follow = None

        self.follow_counter -= 1