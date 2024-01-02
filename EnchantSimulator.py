import random


# TODO 플레이어는 N강에 도달하면 스탑한다.
# TODO 플레이어는 목표 달성 확률이 50%보다 높으면 도전한다.
# 분포도 구하는 시뮬레이션
def getBinomialDistribution(
    enchantTable,
    currentEnchantLevel,
    lowerLimitEnchantLevel,
    try_count,
    upperLimitEnchantLevel,
):
    success_rate = enchantTable[currentEnchantLevel]["success_rate"]
    failure_penalty = enchantTable[currentEnchantLevel]["failure_penalty"]
    repair_rate = enchantTable[currentEnchantLevel]["repair_rate"]
    # 장비 고유
    successReward = enchantTable[currentEnchantLevel]["success_reward"]

    simulation_count = 10000

    result_table = {}

    for simulation in range(simulation_count):
        _currentEnchantLevel = currentEnchantLevel
        for tryout in range(try_count):
            tempRandom = random.random()
            if success_rate >= tempRandom:
                if _currentEnchantLevel + successReward < upperLimitEnchantLevel:
                    _currentEnchantLevel += successReward
                    continue
                else:
                    # 시뮬레이션 중 upperlimit 에 걸리는 경우
                    _currentEnchantLevel = upperLimitEnchantLevel
                    # print("강화 성공하였고 강화 한계치에 걸려 강화 레벨이 강화 한계치로 지정되었습니다.")
                    continue
            # 실패한 경우
            else:
                tempRandom = random.random()
                if repair_rate >= tempRandom:
                    # 복구 성공 시 강화가 떨어지지 않는다.
                    continue
                else:
                    _currentEnchantLevel += failure_penalty
                    if _currentEnchantLevel < lowerLimitEnchantLevel:
                        _currentEnchantLevel = lowerLimitEnchantLevel
                        continue
        # print("result enchantLevel : ", _currentEnchantLevel)
        # 결과 기록하는 부분
        if _currentEnchantLevel in result_table:
            result_table[_currentEnchantLevel] = (
                result_table[_currentEnchantLevel] + 1 / simulation_count
            )
        else:
            result_table[_currentEnchantLevel] = 1 / simulation_count

    # sorted_keys = sorted(result_table.keys())
    # print("total simulation_count : ", simulation_count)
    return result_table


# 목표 강화 수치 이상 달성 확률을 계산한다.
# 시뮬레이션 중 목표 강화 수치 이상 달성시 시뮬레이션 중단.
def get_rate_of_reaching_targetEnchantLevel(
    enchantTable,
    currentEnchantLevel,
    lowerLimitEnchantLevel,
    upperLimitEnchantLevel,
    max_try_count,
    targetEnchantLevel,
):
    simulation_count = 10000

    result_table = {}

    for simulation in range(simulation_count):
        _currentEnchantLevel = currentEnchantLevel
        for tryout in range(max_try_count):
            success_rate = enchantTable[_currentEnchantLevel]["success_rate"]
            failure_penalty = enchantTable[_currentEnchantLevel]["failure_penalty"]
            success_rate = enchantTable[_currentEnchantLevel]["success_rate"]
            repair_rate = enchantTable[_currentEnchantLevel]["repair_rate"]
            successReward = enchantTable[_currentEnchantLevel]["success_reward"]

            tempRandom = random.random()

            if success_rate >= tempRandom:
                # print("강화 성공!")
                _currentEnchantLevel += successReward
                if _currentEnchantLevel > upperLimitEnchantLevel:
                    # print("강화 상한에 도달하여 더이상 강화 레벨이 올라가지 않습니다.")
                    _currentEnchantLevel = upperLimitEnchantLevel
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
                    _currentEnchantLevel += failure_penalty
                    if _currentEnchantLevel < lowerLimitEnchantLevel:
                        # print("강화 하한에 도달하여 더이상 강화 레벨이 내려가지 않습니다.")
                        _currentEnchantLevel = lowerLimitEnchantLevel
        # 결과 기록
        if _currentEnchantLevel in result_table:
            result_table[_currentEnchantLevel] = result_table[_currentEnchantLevel] + (
                1 / simulation_count
            )

        else:
            result_table[_currentEnchantLevel] = 1 / simulation_count

    return result_table


# import ExcelImporter


# class EnchantData:
#     enchantTable = {}

#     def __init__(self):
#         self.enchantTable = ExcelImporter.build_enchantData()


# enchantData = EnchantData()

# result_dict = get_rate_of_reaching_targetEnchantLevel(
#     enchantData.enchantTable["equipment0"],
#     0,
#     0,
#     10,
#     30,
#     10,
# )


# sorted_key_list = sorted(result_dict.keys())
# for key in sorted_key_list:
#     print(key, result_dict[key])
