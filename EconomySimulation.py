from math import comb
import random
import EnchantSimulator
import ExcelImporter
from ExcelImporter import CustomDataFrame


class Player:
    # 인벤토리
    # key : count
    key = ""
    item_dict = {}
    equipment_list = []

    def __init__(self, key, item_dict, equipment_list):
        self.key = key
        self.item_dict = item_dict
        self.equipment_list = equipment_list

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
            print(" ------ choosing Hunting Field : ", huntingField.key)
            for gaining in huntingField.getPredictedGainings():
                if gaining[0] in predicted_item_dict:
                    predicted_item_dict[gaining[0]] += gaining[1]
                else:
                    predicted_item_dict[gaining[0]] = gaining[1]
            # 그 사냥터에서 성장할 수 있는 기댓값 찾기(획득 가능한 재화를 획득했다고 쳤을 때 성장 기댓값 계산)
            # 강화 가능한 장비류 수집
            # 예상 획득 재화를 토대로 계산
            result = self.getBestExpectedEnchantEquipment(predicted_item_dict)
            # 성장할 수 있을 때만 의미있다.
            if result["growth"] > 0:
                equipment = result["equipment"]
                expectedGrowth = result["growth"]
                enchantLevel = result["enchantlevel"]
                tryCount = result["tryCount"]
            else:
                print(
                    "강화의 기댓값이 0 이하이기 때문에 강화하지 않습ㄴ디ㅏ.",
                    result["equipment"],
                    result["growth"],
                )
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

    # TODO EXPECTEDGRWOTH가 0 아래로 내려가면 그만둔다.
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
        print("try_count", try_count)

        if (
            equipment.enchantLevel
            + try_count
            * equipment.enchantTable[equipment.enchantLevel]["success_reward"]
            < targetEnchantLevel
        ):
            #  불가능한 케이스이므로 리턴
            print("모든 강화를 성공하더라도 목표 강화 레벨에 도달할 수 없습니다.")
            return

        # TODO trycount 가 0일 때 처리
        if try_count == 0:
            return
        expectedGrowthFromEquipment = equipment.calculateExpectedGrowth(
            try_count, targetEnchantLevel
        )
        expectedGrowthFromTryCount_tryCount = try_count
        #  TODO 나중에 deprecate this
        # expectedGrowthFromTryCount = 0
        # expectedGrowthFromTryCount_tryCount = 0
        # for current_try in range(try_count):
        #     current_try += 1
        #     print("current_try", current_try)
        #     current_expectedGrowth = equipment.calculateExpectedGrowth(
        #         current_try, targetEnchantLevel
        #     )
        #     print(
        #         "current_expectedGrowth, equipment, targetEnchantLevel, current_try : ",
        #         current_expectedGrowth,
        #         equipment.key,
        #         targetEnchantLevel,
        #         current_try,
        #     )
        #     if current_expectedGrowth >= expectedGrowthFromTryCount:
        #         expectedGrowthFromTryCount = current_expectedGrowth
        #         expectedGrowthFromTryCount_tryCount = current_try
        # if expectedGrowthFromTryCount >= expectedGrowthFromEquipment:
        #     expectedGrowthFromEquipment = expectedGrowthFromTryCount

        return expectedGrowthFromEquipment, expectedGrowthFromTryCount_tryCount

    # 예상 성장치 따져보고 선택한다.
    # 보유한 장비 중 가장 잘 성장할 것 같은 장비를 반환
    # TODO 하나가 아니라 줄 세울까(강화를 두 종류 할 수도 있으니까)
    def getBestExpectedEnchantEquipment(self, item_dict):
        expectedGrowthFromEquipment = 0
        expectedGrowthFromEquipment_equipment = None
        expectedGrowthFromEquipment_enchantLevel = 0
        expectedGrowthFromEquipment_tryCount = 0
        for equipment in self.equipment_list:
            print("================ for equipment", equipment.key)
            if not (equipment.isEnchantable(self)):
                continue
            expectedGrowthFromEnchantLevel = 0
            expectedGrowthFromEnchantLevel_enchantLevel = 0
            expectedGrowthFromEnchantLevel_tryCount = 0
            # TODO trycount 가 1인데 밑 리스트 크기가 2이상이면 불가능한 상황이다. 해결 필요
            for _targetenchantLevel in range(
                equipment.enchantLevel + 1, equipment.upperLimitEnchantLevel + 1
            ):
                print("_targetenchantLevel", _targetenchantLevel)
                expectedGrowthFromEnchantLevel_tuple = (
                    self.calculateExpectedGrowthFromEquipmentEnchant(
                        equipment, _targetenchantLevel, item_dict
                    )
                )
                if expectedGrowthFromEnchantLevel_tuple is None:
                    # 장비 강화가 불가능한 케이스
                    # 재료가 모자라서 강화 못하는 케이스
                    # 현실적으로 불가능한 케이스
                    continue
                else:
                    print(
                        "expectedGrowthFromEnchantLevel_tuple",
                        expectedGrowthFromEnchantLevel_tuple,
                    )
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
        for equipment in self.equipment_list:
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
    upperLimitEnchantLevel = 10
    enchantTable = {}

    def __init__(
        self, key, enchantTable, lowerLimitEnchantLevel, upperLimitEnchantLevel
    ):
        self.key = key
        self.enchantTable = enchantTable
        self.lowerLimitEnchantLevel = lowerLimitEnchantLevel
        self.upperLimitEnchantLevel = upperLimitEnchantLevel

    def doEnchant(self):
        print(
            "now enchant equipment",
            self.key,
            "current enchant level : ",
            self.enchantLevel,
        )
        # 성공 케이스
        if self.enchantTable[self.enchantLevel]["success_rate"] >= random.random():
            self.enchantLevel += self.enchantTable[self.enchantLevel]["success_reward"]
            print("enchant success. current enchant level : ", self.enchantLevel)
        else:
            if (
                self.enchantLevel
                + self.enchantTable[self.enchantLevel]["failure_penalty"]
                >= self.lowerLimitEnchantLevel
            ):
                if (
                    self.enchantTable[self.enchantLevel]["repair_rate"]
                    >= random.random()
                ):
                    print("enchant failed. but repair success: ", self.enchantLevel)
                else:
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
        # 강화 결과 성공 시(양수가 나오는) 기대 성장치 합계
        # TODO 강화 성공 한계 치 등록 필요
        # 강화 결과 실패 시(음수가 나오는) 기대 성장치 합계
        # TODO 강화 실패 한계 치 등록 필요
        print(
            "targetEnchantLevel, self.upperLimitEnchantLevel",
            targetEnchantLevel,
            self.upperLimitEnchantLevel,
        )
        if targetEnchantLevel > self.upperLimitEnchantLevel:
            raise Exception("앞에서 걸러졌어야 한다.")
            print(
                "targetEnchantLevel > self.upperLimitEnchantLevel 라서 targetEnchantLevel을 조정합니다. targetEnchantLevel : ",
                targetEnchantLevel,
            )
            targetEnchantLevel = self.upperLimitEnchantLevel
        print(
            "self.enchantLevel, targetEnchantLevel",
            self.enchantLevel,
            targetEnchantLevel,
        )
        # print("for _targetEnchantLevel in range(targetEnchantLevel):")
        expectedBattlePoint = 0
        expectedGrowth = 0

        result_table = EnchantSimulator.get_rate_of_reaching_targetEnchantLevel(
            self.enchantTable,
            self.enchantLevel,
            self.lowerLimitEnchantLevel,
            self.upperLimitEnchantLevel,
            try_count,
            targetEnchantLevel,
        )
        for _enchantLevel in sorted(result_table.keys()):
            expectedBattlePoint += (
                self.getBattlePointOfLevel(_enchantLevel) * result_table[_enchantLevel]
            )

        expectedGrowth = expectedBattlePoint - self.getBattlePointOfLevel(
            self.enchantLevel
        )
        print("expectedGrowth", expectedGrowth)

        return expectedGrowth

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

    def setInitLevel(self, level):
        self.enchantLevel = level


class HuntingField:
    # item, count, rate
    key = ""
    gaining_list = []
    battlePointLimit = 0

    def __init__(self, key, tuple, tuple1, tuple2):
        self.gaining_list = [tuple, tuple1, tuple2]
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


class SimulationManager:
    currentTurn = 0
    player_List = None
    huntingField_list = []
    enchantData = {}
    equipmentData_dict = {}
    equipment_dict = {}

    def __init__(self):
        huntingField_dict = ExcelImporter.build_huntingFieldData()
        self.huntingField_list = []
        for _huntingField_key in huntingField_dict.keys():
            _huntingField_dict = huntingField_dict[_huntingField_key]
            self.huntingField_list.append(
                HuntingField(
                    _huntingField_key,
                    (
                        _huntingField_dict["gaining0"],
                        _huntingField_dict["count0"],
                        _huntingField_dict["rate0"],
                    ),
                    (
                        _huntingField_dict["gaining1"],
                        _huntingField_dict["count1"],
                        _huntingField_dict["rate1"],
                    ),
                    (
                        _huntingField_dict["gaining2"],
                        _huntingField_dict["count2"],
                        _huntingField_dict["rate2"],
                    ),
                )
            )
        self.enchantData = EnchantData()
        equipmentData_dict = {}
        equipmentData_dict = ExcelImporter.build_equipmentData()
        equipment_dict = {}
        for equipment_key in equipmentData_dict.keys():
            equipment_dict[equipment_key] = Equipment(
                equipment_key,
                self.enchantData.enchantTable[equipment_key],
                equipmentData_dict[equipment_key]["lowerLimitEnchantLevel"],
                equipmentData_dict[equipment_key]["upperLimitEnchantLevel"],
            )

        player_dict = ExcelImporter.build_playerData()
        for _player in player_dict.keys():
            _player_dict = player_dict[_player]
            player = Player(
                _player,
                {
                    _player_dict["item0"]: _player_dict["count0"],
                    _player_dict["item1"]: _player_dict["count1"],
                    _player_dict["item2"]: _player_dict["count2"],
                },
                [
                    equipment_dict[_player_dict["equipment0"]],
                    equipment_dict[_player_dict["equipment1"]],
                    equipment_dict[_player_dict["equipment2"]],
                ],
            )
            for equipment in player.equipment_list:
                equipment.setInitLevel(_player_dict["equipment0_level"])

            self.player_List = []
            self.player_List.append(player)

    def processTurn(self, turn, customDataFrame):
        # n회 루프하도록 한다.
        for player in self.player_List:
            chosenHuntingField = player.chooseHuntingField(self.huntingField_list)
            print("player.chooseHuntingField", chosenHuntingField.key)
            chosenHuntingField.giveItem(player)
            # TODO 강화할 게 없을 때까지 강화시도 한다.
            while True:
                print("----now find getBestExpectedEnchantEquipment")

                best_enchant_info = player.getBestExpectedEnchantEquipment(
                    player.item_dict
                )
                growth = best_enchant_info["growth"]
                if growth > 0:
                    best_enchant_info_equipment = best_enchant_info["equipment"]
                else:
                    print(
                        "강화 기대 성장치가 0 이하이므로 강화하지 않습니다(선택하지 않습니다.)",
                        best_enchant_info["equipment"],
                        best_enchant_info["growth"],
                    )
                    break
                # TODO 리팩토링 필요
                if best_enchant_info_equipment is not None:
                    equipment_key = best_enchant_info_equipment.key
                    enchant_level = best_enchant_info_equipment.enchantLevel
                    print(
                        f"Best Expected Enchant Equipment equipment_key, current enchantLevel: {equipment_key} {enchant_level}"
                    )

                    if best_enchant_info_equipment.isEnchantable(player):
                        player.runEnchant(best_enchant_info_equipment)
                    else:
                        print("Cannot enchant the selected equipment.")
                else:
                    print("No more enchantable equipment with expected growth.")
                    break

            # TODO 좀더 똑똑하게
            _player_key = player.key
            _item0 = list(player.item_dict.items())[0][0]
            _count0 = list(player.item_dict.items())[0][1]
            _item1 = list(player.item_dict.items())[1][0]
            _count1 = list(player.item_dict.items())[1][1]
            _item2 = list(player.item_dict.items())[2][0]
            _count2 = list(player.item_dict.items())[2][1]
            _equipment0 = player.equipment_list[0].key
            _equipment_level0 = player.equipment_list[0].enchantLevel
            _equipment1 = player.equipment_list[1].key
            _equipment_level1 = player.equipment_list[1].enchantLevel
            _equipment2 = player.equipment_list[2].key
            _equipment_level2 = player.equipment_list[2].enchantLevel

            customDataFrame.build_dataFrame(
                turn,
                _player_key,
                _item0,
                _count0,
                _item1,
                _count1,
                _item2,
                _count2,
                _equipment0,
                _equipment_level0,
                _equipment1,
                _equipment_level1,
                _equipment2,
                _equipment_level2,
            )


def __main__():
    simulationManager = SimulationManager()
    customDataFrame = CustomDataFrame()
    for current_turn in range(1, 10):
        print("----------------- ---------------------current_turn : ", current_turn)
        simulationManager.processTurn(current_turn, customDataFrame)
    customDataFrame.exportToExcel()


__main__()
