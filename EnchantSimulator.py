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


# 목표 강화 수치 이상 달성시 스탑
def getRateOfEnchantLevel(
    enchantTable,
    currentEnchantLevel,
    lowerLimitEnchantLevel,
    try_count,
    targetEnchantLevel,
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
                if _currentEnchantLevel >= targetEnchantLevel:
                    break
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
        # 결과 기록
        if _currentEnchantLevel in result_table:
            result_table[_currentEnchantLevel] = result_table[_currentEnchantLevel] + 1
        else:
            result_table[_currentEnchantLevel] = 1
    print(result_table.items())
    input()


def calculateTargetEnchantLevelSuccessPercent(
    enchantType, try_Count, targetEnchantLevel, success_Percent
):
    # TODO 아래는 뒷걸음칠 곳이 무한대일 때의 확률이다. 0강 이하로 내려가지 않는 경우에는 다른 확률이 필요하다!
    if enchantType == "penalty1":
        # 검증하는 곳(짝수 + 짝수 또는 홀수 + 홀수 쌍만 나오도록 검증)
        if try_Count % 2 == 0:
            if targetEnchantLevel % 2 != 0:
                raise Exception("시도 횟수가 짝수면 목표 강화 횟수도 짝수여야 합니다")
        else:
            if targetEnchantLevel % 2 != 1:
                raise Exception("시도 횟수가 홀수면 목표 강화 횟수도 홀수여야 합니다")

        combination_Count = comb(try_Count - 2, (try_Count + targetEnchantLevel) / 2)
        return (
            success_Percent ** ((try_Count + targetEnchantLevel) / 2)
            * (1 - success_Percent) ** ((try_Count - targetEnchantLevel) / 2)
            * combination_Count
        )
