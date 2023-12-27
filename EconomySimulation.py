from math import comb
import random
import EnchantSimulator


class Player:
    # 인벤토리
    # key : count
    item_dict = {}
    equipment_List = []

    def __init__(self, equipment_List):
        self.item_dict = None
        self.equipment_List = equipment_List

    def chooseHuntingField(self, huntingField_list):
        # 사용 가능한 사냥터 찾기
        _enterableHuntingField_List = []
        for huntingField in huntingField_list:
            if huntingField.isPlayerEnterable(self):
                _enterableHuntingField_List.append(huntingField)

        # 그 사냥터에서 획득 가능한 재화 찾기
        expectedGrowthFromHuntingField = 0
        expectedGrowthFromHuntingField_huntingField = None
        for huntingField in _enterableHuntingField_List:
            huntingField.getPredictedGainings()
            # 그 사냥터에서 성장할 수 있는 기댓값 찾기(획득 가능한 재화를 획득했다고 쳤을 때 성장 기댓값 계산)
            # 강화 가능한 장비류 수집
            expectedGrowthFromEquipment = 0
            expectedGrowthFromEquipment_equipment = None
            for equipment in self.equipment_List:
                # TODO write TargetEnchantLEvel please
                expectedGrowthFromTryCount_tuple = (
                    self.calculateExpectedGrowthFromEquipmentEnchant(equipment, 10)
                )
                if expectedGrowthFromTryCount_tuple is not None:
                    expectedGrowthFromTryCount = expectedGrowthFromTryCount_tuple[0]
                else:
                    raise Exception()
                # try_count는 굳이 필요 없을 것 같아서 저장 안 함
                if expectedGrowthFromTryCount >= expectedGrowthFromEquipment:
                    expectedGrowthFromEquipment = expectedGrowthFromTryCount
                    expectedGrowthFromEquipment_equipment = equipment
            if expectedGrowthFromEquipment >= expectedGrowthFromHuntingField:
                expectedGrowthFromHuntingField = expectedGrowthFromEquipment
                expectedGrowthFromHuntingField_huntingField = huntingField
            return expectedGrowthFromHuntingField_huntingField

        # 그 기댓값들의 최대값의 사냥터를 반환
        return huntingField

    def calculateExpectedGrowthFromEquipmentEnchant(
        self, equipment, targetEnchantLevel
    ):
        expectedGrowthFromEquipment = 0
        if not (equipment.isEnchantable(self)):
            print("해당 장비는 강화 불가능합니다.")
            return
        if equipment.enchantLevel >= targetEnchantLevel:
            print("목표 강화 레벨과 현재 강화 레벨이 동일하여 강화할 수 없습니다.")
            return
        # 강화 시도할 개수
        try_count = 0
        for tuple in equipment.getEnchantRecipe():
            enchantMaterial = tuple[0]
            enchantMaterial_count = tuple[1]
            # 강화 재료 종류 별로 만들 수 있는 값 중 가장 작은 값이 제작할 수 있는 개수다.
            if enchantMaterial in self.item_dict:
                try_count = min(
                    try_count, self.item_dict[enchantMaterial] // enchantMaterial_count
                )
        expectedGrowthFromTryCount = 0
        expectedGrowthFromTryCount_tryCount = 0
        for current_try in range(try_count):
            # 몇 회 시도하는 게 최선인지 알 수 없으니 try_count가 n이라면 1~n까지 시도한 경우의 수를 모두 따지고 그중 가장 큰 값을 가져가자!
            targetEnchantLevel = current_try
            current_expectedGrowth = equipment.calculateExpectedGrowth(
                current_try, targetEnchantLevel
            )
            if current_expectedGrowth >= expectedGrowthFromTryCount:
                expectedGrowthFromTryCount = current_expectedGrowth
                expectedGrowthFromTryCount_tryCount = current_try
        if expectedGrowthFromTryCount >= expectedGrowthFromEquipment:
            expectedGrowthFromEquipment = expectedGrowthFromTryCount
        return expectedGrowthFromEquipment, expectedGrowthFromTryCount_tryCount

    # 예상 성장치 따져보고 선택한다.
    def getBestExpectedEnchantEquipment(self):
        expectedGrowthFromEquipment = 0
        expectedGrowthFromEquipment_equipment = None
        for equipment in self.equipment_List:
            # TODO write TargetEnchantLEvel please
            expectedGrowthFromTryCount_tuple = (
                self.calculateExpectedGrowthFromEquipmentEnchant(equipment, 10)
            )
            expectedGrowthFromTryCount = expectedGrowthFromTryCount_tuple[0]
            # try_count는 굳이 필요 없을 것 같아서 저장 안 함
            if expectedGrowthFromTryCount >= expectedGrowthFromEquipment:
                expectedGrowthFromEquipment = expectedGrowthFromTryCount
                expectedGrowthFromEquipment_equipment = equipment

        return equipment

    def runEnchant(equipment):
        # TODO 인벤토리에서 재화 차감
        # 실제 강화
        equipment.doEnchant()

    def getBattlePoint(self):
        _battlePoint = 0
        for equipment in self.equipment_List:
            _battlePoint = _battlePoint + equipment.getBattlePoint()
        return _battlePoint

    def acquire_item(self, item, count):
        self.item_dict[item] += count

    # 보유하고 있는 장비 기반으로 아이템의 가치 산정
    def calculateValue(item):
        pass


# 재화
class Item:
    def __init__():
        pass


class EnchantData:
    enchantTable = {}

    def __init__(self):
        self.enchantTable = {
            "equipment0": {
                0: {
                    "dd": 0,
                    "pv": 0,
                    "hp": 0,
                    "success_rate": 0.1,
                    "failure_penalty": -1,
                    "repair_rate": 0.8,
                    "enchantRecipe": [(1, 1), (1, 1), (1, 1)],
                },
                1: {
                    "dd": 0,
                    "pv": 0,
                    "hp": 0,
                    "success_rate": 0.1,
                    "failure_penalty": -1,
                    "repair_rate": 0.8,
                    "enchantRecipe": [(1, 1), (1, 1), (1, 1)],
                },
                2: {
                    "dd": 0,
                    "pv": 0,
                    "hp": 0,
                    "success_rate": 0.1,
                    "failure_penalty": -1,
                    "repair_rate": 0.8,
                    "enchantRecipe": [(1, 1), (1, 1), (1, 1)],
                },
                3: {
                    "dd": 0,
                    "pv": 0,
                    "hp": 0,
                    "success_rate": 0.1,
                    "failure_penalty": -1,
                    "repair_rate": 0.8,
                    "enchantRecipe": [(1, 1), (1, 1), (1, 1)],
                },
            }
        }


# 장비
class Equipment:
    equipment_key = ""
    enchantLevel = 0
    enchantType = "penalty1"
    lowerLimitEnchantLevel = 0
    enchantTable = {}

    def __init__(self, equipment_key, enchantLevel, enchantType, enchantTable):
        self.equipment_key = equipment_key
        self.enchantLevel = enchantLevel
        self.enchantType = enchantType
        self.enchantTable = enchantTable

    def doEnchant():
        # 성공 시 강화 단계 상승
        # 실패 시 아무일도 일어나지 않음 또는 강화 단계 하락
        pass

    def getEnchantRecipe(self):
        return self.enchantTable[self.enchantLevel]["enchantRecipe"]

    # 시행 횟수 - 강화 확률 토대로 계산
    def calculateExpectedGrowth(self, try_count, targetEnchantLevel):
        success_Percent = self.enchantTable[targetEnchantLevel - 1]
        _expectedGrowth = 0
        # 강화 결과 성공 시(양수가 나오는) 기대 성장치 합계
        # TODO 강화 성공 한계 치 등록 필요
        for _targetEnchantLevel in range(targetEnchantLevel):
            _expectedGrowth = (
                _expectedGrowth
                + self.enchantTable[_targetEnchantLevel]
                * Calculator.calculateTargetEnchantLevelSuccessPercent(
                    self.enchantType, try_count, _targetEnchantLevel, success_Percent
                )
                - self.enchantTable[self.enchantLevel]
            )
        # 강화 결과 실패 시(음수가 나오는) 기대 성장치 합계
        # TODO 강화 실패 한계 치 등록 필요
        for _targetEnchantLevel in range(targetEnchantLevel):
            # success_Percent를 1의 보수로 바꿨다.
            _expectedGrowth = (
                _expectedGrowth
                + self.enchantTable[_targetEnchantLevel]
                * Calculator.calculateTargetEnchantLevelSuccessPercent(
                    self.enchantType,
                    try_count,
                    _targetEnchantLevel,
                    1 - success_Percent,
                )
                - self.enchantTable[self.enchantLevel]
            )
        return _expectedGrowth

    def isEnchantable(self, player):
        return True

    # 외부에서 주어진 테이블 대로
    def getBattlePoint(self):
        print(self.enchantTable.items())
        return (
            self.enchantTable[self.enchantLevel]["dd"]
            + self.enchantTable[self.enchantLevel]["pv"]
        )


class Calculator:
    pass


class SimulationManager:
    currentTurn = 0
    player_List = None
    huntingField_list = []
    enchantData = {}

    # TODO 외부로 빼기 엑셀 같은 데
    def __init__(self):
        self.huntingField_list = [
            HuntingField((0, 10, 1), (1, 13, 1), (2, 20, 1)),
            HuntingField((0, 10, 1), (1, 13, 1), (2, 20, 1)),
            HuntingField((0, 10, 1), (1, 13, 1), (2, 20, 1)),
        ]
        self.enchantData = EnchantData()
        self.player_List = [
            Player(
                [
                    Equipment(
                        "equipment0",
                        1,
                        "penalty1",
                        self.enchantData.enchantTable["equipment0"],
                    ),
                    Equipment(
                        "equipment0",
                        1,
                        "penalty1",
                        self.enchantData.enchantTable["equipment0"],
                    ),
                    Equipment(
                        "equipment0",
                        1,
                        "penalty1",
                        self.enchantData.enchantTable["equipment0"],
                    ),
                ]
            )
        ]

    def processTurn(self):
        # n회 루프하도록 한다.
        print("processTurn")
        for player in self.player_List:
            chosenHuntingField = player.chooseHuntingField(self.huntingField_list)
            print("player.chooseHuntingField", chosenHuntingField)
            chosenHuntingField.giveItem(player)
            print("player received Item")
            player.runEnchant(player.getBestExpectedEnchantEquipment())
            print(player.getBattlePoint())


class HuntingField:
    # item, count, rate
    gaining_list = [(0, 0, 1), (0, 0, 1), (0, 0, 1)]
    battlePointLimit = 0

    def __init__(self, tuple, tuple1, tuple2):
        self.gaining_list.append(tuple)
        self.gaining_list.append(tuple1)
        self.gaining_list.append(tuple2)

    def isPlayerEnterable(self, player):
        return player.getBattlePoint() >= self.battlePointLimit

    def giveItem(self, player):
        # TODO self.gaining_list 에서 적절히 거른 결과물을 지급하자
        for gaining in self.gaining_list:
            # 확률적으로 지급
            if gaining[2] >= random.random():
                player.acquire_item((gaining[0], gaining[1]))
            else:
                continue

    # itemkey, expectedcount 쌍 리스트 반환
    def getPredictedGainings(self):
        rv_list = []
        for gaining in self.gaining_list:
            # itemkey, itemcount * rate
            rv_list.append((gaining[0], gaining[1] * gaining[2]))

        return rv_list


def __main__():
    simulationManager = SimulationManager()
    simulationManager.processTurn()


__main__()
