import random


# TODO 플레이어는 N강에 도달하면 스탑한다.
# TODO 플레이어는 목표 달성 확률이 50%보다 높으면 도전한다.
# 분포도 구하는 시뮬레이션
def getBinomialDistribution(
    enchantTable, currentEnchantLevel, lowerLimitEnchantLevel, try_count
):
    success_rate = enchantTable[currentEnchantLevel]["success_rate"]
    failurePenalty = enchantTable[currentEnchantLevel]["failure_penalty"]
    success_rate = enchantTable[currentEnchantLevel]["success_rate"]
    repair_rate = enchantTable[currentEnchantLevel]["repair_rate"]
    # 장비 고유
    successReward = 1

    simulation_count = 1000000

    result_table = {}

    for simulation in range(simulation_count):
        _currentEnchantLevel = currentEnchantLevel
        for tryout in range(try_count):
            tempRandom = random.random()
            if success_rate >= tempRandom:
                _currentEnchantLevel += successReward
            # 실패한 경우
            else:
                tempRandom = random.random()
                if repair_rate >= tempRandom:
                    # 복구 성공 시 강화가 떨어지지 않는다.
                    continue
                else:
                    _currentEnchantLevel += failurePenalty
                    if _currentEnchantLevel < lowerLimitEnchantLevel:
                        _currentEnchantLevel = lowerLimitEnchantLevel
        # print("result enchantLevel : ", _currentEnchantLevel)
        if _currentEnchantLevel in result_table:
            result_table[_currentEnchantLevel] = result_table[_currentEnchantLevel] + 1
        else:
            result_table[_currentEnchantLevel] = 1

    sorted_keys = sorted(result_table.keys())
    print("total simulation_count : ", simulation_count)
    for key in sorted_keys:
        print(
            key, ":", result_table[key], result_table[key] * 100 / simulation_count, "%"
        )
    input()


# 목표 강화 수치 이상 달성 확률을 계산한다. get_probability_of_reaching_target
# 목표 강화 수치 이상 달성시 스탑
def getRateOfReachingEnchantLevel(
    enchantTable,
    currentEnchantLevel,
    lowerLimitEnchantLevel,
    max_try_count,
    targetEnchantLevel,
):
    rateOfReachingEnchantLevel = 0

    success_rate = enchantTable[currentEnchantLevel]["success_rate"]
    failurePenalty = enchantTable[currentEnchantLevel]["failure_penalty"]
    success_rate = enchantTable[currentEnchantLevel]["success_rate"]
    repair_rate = enchantTable[currentEnchantLevel]["repair_rate"]
    # 장비 고유
    successReward = 1

    simulation_count = 2

    result_table = {}

    for simulation in range(simulation_count):
        _currentEnchantLevel = currentEnchantLevel
        for tryout in range(max_try_count):
            tempRandom = random.random()
            if success_rate >= tempRandom:
                _currentEnchantLevel += successReward
                if _currentEnchantLevel >= targetEnchantLevel:
                    break
            # 실패한 경우
            else:
                tempRandom = random.random()
                if repair_rate >= tempRandom:
                    # 복구 성공 시 강화가 떨어지지 않는다.
                    # print("복구 성공!")
                    continue
                else:
                    _currentEnchantLevel += failurePenalty
                    if _currentEnchantLevel < lowerLimitEnchantLevel:
                        # print("하한선에 도달하여 더이상 강화 레벨이 내려가지 않습니다.")
                        _currentEnchantLevel = lowerLimitEnchantLevel
        # print("result enchantLevel : ", _currentEnchantLevel)
        # 결과 기록
        if _currentEnchantLevel in result_table:
            result_table[_currentEnchantLevel] = result_table[_currentEnchantLevel] + 1
        else:
            result_table[_currentEnchantLevel] = 1

        sorted_keys = sorted(result_table.keys())
        for enchantLevel in sorted_keys:
            if enchantLevel <= targetEnchantLevel:
                rateOfReachingEnchantLevel += result_table[enchantLevel]
            else:
                # 키가 정렬되어 있으므로 브레이크한다.
                break
        return rateOfReachingEnchantLevel


def findOrderedPair(player, equipment_List):
    item_dict = player.item_dict
    equipment_List = equipment_List
    orderedPair_list = []
    for equipment in equipment_List:
        enchantLevel = equipment.enchantLevel
        enchantTable = equipment.enchantTable
