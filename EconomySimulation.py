from math import comb
import random
import EnchantSimulator
import ExcelImporter


class Player:
    # 인벤토리
    # key : count
    item_dict = {}
    equipment_List = []

    def __init__(self, item_dict, equipment_List):
        self.item_dict = item_dict
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

        predicted_item_dict = self.item_dict.copy()
        for huntingField in _enterableHuntingField_List:
            for gaining in huntingField.getPredictedGainings():
                if gaining[0] in predicted_item_dict:
                    predicted_item_dict[gaining[0]] += gaining[1]
                else:
                    predicted_item_dict[gaining[0]] = gaining[1]
            # 그 사냥터에서 성장할 수 있는 기댓값 찾기(획득 가능한 재화를 획득했다고 쳤을 때 성장 기댓값 계산)
            # 강화 가능한 장비류 수집
            # 예상 획득 재화를 토대로 계산
            result = self.getBestExpectedEnchantEquipment(predicted_item_dict)
            equipment = result["equipment"]
            expectedGrowth = result["growth"]
            enchantLevel = result["enchantlevel"]
            tryCount = result["tryCount"]
            # print(
            #     "최선의 강화 장비 : equipment.key, expectedGrowth, enchantLevel, tryCount",
            #     equipment.key,
            #     expectedGrowth,
            #     enchantLevel,
            #     tryCount,
            # )
            if equipment is None:
                # 강화할 것이 없을 때는 넘긴다.
                continue
            print(
                "getBestExpectedEnchantEquipment 결과 : ", result["equipment"].key, result
            )
            expectedGrowthFromEquipment = expectedGrowth
            if expectedGrowthFromEquipment >= expectedGrowthFromHuntingField:
                expectedGrowthFromHuntingField = expectedGrowthFromEquipment
                expectedGrowthFromHuntingField_huntingField = huntingField
            return expectedGrowthFromHuntingField_huntingField

        # 그 기댓값들의 최대값의 사냥터를 반환
        return huntingField

    def calculateExpectedGrowthFromEquipmentEnchant(
        self, equipment, targetEnchantLevel, item_dict
    ):
        expectedGrowthFromEquipment = 0
        if not (equipment.isEnchantable(self)):
            print("해당 장비는 강화 불가능합니다.")
            return
        if equipment.enchantLevel >= targetEnchantLevel:
            print("목표 강화 레벨과 현재 강화 레벨이 동일하여 강화할 수 없습니다.")
            return
        # 강화 시도할 개수
        try_count = -1
        for tuple in equipment.getEnchantRecipe(equipment.enchantLevel):
            enchantMaterial = tuple[0]
            enchantMaterial_count = tuple[1]
            # 강화 재료 종류 별로 만들 수 있는 값 중 가장 작은 값이 제작할 수 있는 개수다.
            if enchantMaterial in item_dict:
                _try_count = item_dict[enchantMaterial] // enchantMaterial_count
                if try_count == -1:
                    try_count = _try_count
                if try_count >= _try_count:
                    try_count = _try_count
        # TODO trycount 가 0일 때 처리
        if try_count == 0:
            return

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
    # 보유한 장비 중 가장 잘 성장할 것 같은 장비를 반환
    # TODO 하나가 아니라 줄 세울까(강화를 두 종류 할 수도 있으니까)
    def getBestExpectedEnchantEquipment(self, item_dict):
        expectedGrowthFromEquipment = 0
        expectedGrowthFromEquipment_equipment = None
        expectedGrowthFromEquipment_enchantLevel = 0
        expectedGrowthFromEquipment_tryCount = 0
        for equipment in self.equipment_List:
            if not (equipment.isEnchantable(self)):
                continue
            expectedGrowthFromEnchantLevel = 0
            expectedGrowthFromEnchantLevel_enchantLevel = 0
            expectedGrowthFromEnchantLevel_tryCount = 0
            for _targetenchantLevel in range(
                equipment.enchantLevel + 1, equipment.upperLimitEnchantLevel
            ):
                expectedGrowthFromEnchantLevel_tuple = (
                    self.calculateExpectedGrowthFromEquipmentEnchant(
                        equipment, _targetenchantLevel, item_dict
                    )
                )
                if expectedGrowthFromEnchantLevel_tuple is None:
                    # 장비 강화가 불가능한 케이스
                    # 재료가 모자라서 강화 못하는 케이스
                    continue
                else:
                    if (
                        expectedGrowthFromEnchantLevel_tuple[0]
                        >= expectedGrowthFromEnchantLevel
                    ):
                        expectedGrowthFromEnchantLevel = (
                            expectedGrowthFromEnchantLevel_tuple[0]
                        )
                        expectedGrowthFromEnchantLevel_enchantLevel = (
                            _targetenchantLevel
                        )
                        expectedGrowthFromEnchantLevel_tryCount = (
                            expectedGrowthFromEnchantLevel_tuple[1]
                        )
            if expectedGrowthFromEnchantLevel >= expectedGrowthFromEquipment:
                expectedGrowthFromEquipment = expectedGrowthFromEnchantLevel
                expectedGrowthFromEquipment_equipment = equipment
                expectedGrowthFromEquipment_enchantLevel = (
                    expectedGrowthFromEnchantLevel_enchantLevel
                )
                expectedGrowthFromEquipment_tryCount = (
                    expectedGrowthFromEnchantLevel_tryCount
                )
        return {
            "equipment": expectedGrowthFromEquipment_equipment,
            "growth": expectedGrowthFromEquipment,
            "enchantlevel": expectedGrowthFromEquipment_enchantLevel,
            "tryCount": expectedGrowthFromEquipment_tryCount,
        }

    def runEnchant(self, equipment):
        # 인벤토리에서 재화 차감
        print("player run enchant", equipment.key)
        print("current player inventory : ", self.item_dict)
        for tuple in equipment.getEnchantRecipe(equipment.enchantLevel):
            enchantMaterial = tuple[0]
            enchantMaterial_count = tuple[1]
            if self.item_dict[enchantMaterial] < enchantMaterial_count:
                # 강화에 필요한 재화가 모자라는 경우
                print("강화에 필요한 재화가 모자랍니다.")
                raise Exception("isenchantable 에서 검증했을 텐데 왜 또 걸릴까")
                return
            else:
                self.item_dict[enchantMaterial] -= enchantMaterial_count
        print("current player inventory : ", self.item_dict)
        # 실제 강화
        equipment.doEnchant()

    def getBattlePoint(self):
        _battlePoint = 0
        for equipment in self.equipment_List:
            _battlePoint = _battlePoint + equipment.getBattlePointOfLevel(
                equipment.enchantLevel
            )
        return _battlePoint

    def acquire_item(self, item, count):
        if item in self.item_dict:
            self.item_dict[item] += count
        else:
            self.item_dict[item] = 0
            self.item_dict[item] += count

    # 보유하고 있는 장비 기반으로 아이템의 가치 산정
    def calculateValue(item):
        pass


# 재화
class Item:
    itemkey = ""

    def __init__(self, itemkey):
        self.itemkey = itemkey


class EnchantData:
    enchantTable = {}

    def __init__(self):
        self.enchantTable = ExcelImporter.build_enchantData()


# 장비
class Equipment:
    key = ""
    enchantLevel = 0
    enchantType = "penalty1"
    lowerLimitEnchantLevel = 0
    upperLimitEnchantLevel = 3
    enchantTable = {}

    def __init__(self, key, enchantLevel, enchantTable):
        self.key = key
        self.enchantLevel = enchantLevel
        self.enchantTable = enchantTable

    def doEnchant(self):
        print(
            "now enchant equipment",
            self.key,
            "current enchant level : ",
            self.enchantLevel,
        )
        if self.enchantTable[self.enchantLevel]["success_rate"] >= random.random():
            self.enchantLevel += self.enchantTable[self.enchantLevel]["success_reward"]
            print("enchant successed. current enchant level : ", self.enchantLevel)
        else:
            if (
                self.enchantLevel
                + self.enchantTable[self.enchantLevel]["failure_penalty"]
                >= self.lowerLimitEnchantLevel
            ):
                self.enchantLevel += self.enchantTable[self.enchantLevel][
                    "failure_penalty"
                ]
                print("enchant failed. current enchant level : ", self.enchantLevel)
            else:
                self.enchantLevel = self.lowerLimitEnchantLevel
                print("enchant failed. but penaly is limited")
        # 성공 시 강화 단계 상승
        # 실패 시 아무일도 일어나지 않음 또는 강화 단계 하락

    def getEnchantRecipe(self, enchantLevel):
        return self.enchantTable[enchantLevel]["enchantRecipe"]

    # 시행 횟수 - 강화 확률 토대로 계산
    def calculateExpectedGrowth(self, try_count, targetEnchantLevel):
        _expectedGrowth = 0
        # 강화 결과 성공 시(양수가 나오는) 기대 성장치 합계
        # TODO 강화 성공 한계 치 등록 필요
        # 강화 결과 실패 시(음수가 나오는) 기대 성장치 합계
        # TODO 강화 실패 한계 치 등록 필요
        if targetEnchantLevel >= self.upperLimitEnchantLevel:
            targetEnchantLevel = self.upperLimitEnchantLevel

        for _targetEnchantLevel in range(targetEnchantLevel):
            _expectedGrowth = (
                self.getBattlePointOfLevel(_targetEnchantLevel)
            ) * EnchantSimulator.getRateOfReachingEnchantLevel(
                self.enchantTable,
                self.enchantLevel,
                0,
                try_count,
                _targetEnchantLevel,
            ) - self.getBattlePointOfLevel(
                self.enchantLevel
            )

        return _expectedGrowth

    def isEnchantable(self, player):
        # 강화 한계치보다 강화가 같거나 높은지
        if self.enchantLevel >= self.upperLimitEnchantLevel:
            return False
        # 재료가 충분히 있는지
        for tuple in self.getEnchantRecipe(self.enchantLevel):
            enchantMaterial = tuple[0]
            enchantMaterial_count = tuple[1]
            if player.item_dict[enchantMaterial] < enchantMaterial_count:
                # 강화에 필요한 재화가 모자라는 경우
                print("강화에 필요한 재화가 모자랍니다.")
                return False
        return True

    # 외부에서 주어진 테이블 대로
    def getBattlePointOfLevel(self, enchantLevel):
        return (
            self.enchantTable[enchantLevel]["dd"]
            + self.enchantTable[enchantLevel]["pv"]
        )


class SimulationManager:
    currentTurn = 0
    player_List = None
    huntingField_list = []
    enchantData = {}

    # TODO 외부로 빼기 엑셀 같은 데
    def __init__(self):
        self.huntingField_list = [
            HuntingField(
                "huntingfield0", ("item0", 10, 1), ("item1", 13, 1), ("item2", 20, 1)
            ),
            HuntingField(
                "huntingfield1", ("item0", 10, 1), ("item1", 13, 1), ("item2", 20, 1)
            ),
            HuntingField(
                "huntingfield2", ("item0", 10, 1), ("item1", 13, 1), ("item2", 20, 1)
            ),
        ]
        self.enchantData = EnchantData()
        player_dict = ExcelImporter.build_playerData()
        for _player in player_dict.keys():
            _player_dict = player_dict[_player]
            player = Player(
                {
                    _player_dict["item0"]: _player_dict["count0"],
                    _player_dict["item1"]: _player_dict["count1"],
                    _player_dict["item2"]: _player_dict["count2"],
                },
                [
                    Equipment(
                        _player_dict["equipment0"],
                        _player_dict["equipment0_level"],
                        self.enchantData.enchantTable[_player_dict["equipment0"]],
                    ),
                    Equipment(
                        _player_dict["equipment1"],
                        _player_dict["equipment1_level"],
                        self.enchantData.enchantTable[_player_dict["equipment1"]],
                    ),
                    Equipment(
                        _player_dict["equipment2"],
                        _player_dict["equipment2_level"],
                        self.enchantData.enchantTable[_player_dict["equipment2"]],
                    ),
                ],
            )
            self.player_List = []
            self.player_List.append(player)

    def processTurn(self):
        # n회 루프하도록 한다.
        print("processTurn")
        for player in self.player_List:
            chosenHuntingField = player.chooseHuntingField(self.huntingField_list)
            print("player.chooseHuntingField", chosenHuntingField.key)
            chosenHuntingField.giveItem(player)
            # TODO 강화할 게 없을 때까지 강화시도 한다.
            while (
                player.getBestExpectedEnchantEquipment(player.item_dict)["equipment"]
                is not None
            ):
                equipment = player.getBestExpectedEnchantEquipment(player.item_dict)[
                    "equipment"
                ]
                print(
                    "best Expected Enchant Equipment : ",
                    equipment.key,
                    equipment.enchantLevel,
                )
                if equipment.isEnchantable(player):
                    player.runEnchant(
                        player.getBestExpectedEnchantEquipment(player.item_dict)[
                            "equipment"
                        ]
                    )
                else:
                    continue
            for equipment in player.equipment_List:
                print(equipment.key, equipment.enchantLevel)
            print("player.getBattlePoint()", player.getBattlePoint())


class HuntingField:
    # item, count, rate
    key = ""
    gaining_list = []
    battlePointLimit = 0

    def __init__(self, key, tuple, tuple1, tuple2):
        self.gaining_list = []
        self.key = key

    def isPlayerEnterable(self, player):
        return player.getBattlePoint() >= self.battlePointLimit

    def giveItem(self, player):
        # TODO self.gaining_list 에서 적절히 거른 결과물을 지급하자
        print("gaining_list : ", self.gaining_list)
        for gaining in self.gaining_list:
            # 확률적으로 지급
            if gaining[2] >= random.random():
                player.acquire_item(gaining[0], gaining[1])
                print("player received Item", gaining[0], gaining[1], "from", self.key)
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
    for current_turn in range(1):
        print("--------------------------------------current_turn : ", current_turn)
        simulationManager.processTurn()


__main__()
