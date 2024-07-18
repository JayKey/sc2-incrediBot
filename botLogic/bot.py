from sc2.bot_ai import BotAI
from botLogic.economy import EconomyManager
from botLogic.defense import DefenseManager
from botLogic.production import ProductionManager
from botLogic.aggression import AggressionManager
from botLogic.camera_manager import CameraManager

class IncrediBot(BotAI):
    def __init__(self):
        self.economy_manager = EconomyManager(self)
        self.defense_manager = DefenseManager(self)
        self.production_manager = ProductionManager(self)
        self.aggression_manager = AggressionManager(self)
        self.camera_manager = CameraManager(self)

    async def on_step(self, iteration: int):
        await self.economy_manager.manage_economy()
        await self.defense_manager.manage_defense()
        await self.production_manager.manage_production()
        await self.aggression_manager.manage_aggression()
        await self.camera_manager.manage_camera()
