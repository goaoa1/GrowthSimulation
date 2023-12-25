import random

# TODO 플레이어는 N강에 도달하면 스탑한다.
# TODO 플레이어는 목표 달성 확률이 50%보다 높으면 도전한다.

try_count = 10
currentEnchantLevel = 0
success_rate = 0.3
failure_penalty = -1
lowerLimitEnchantLevel = 0
repair_rate = 1

simulation_count = 1000000

result_table = {}

for simulation in range(simulation_count):
    _currentEnchantLevel = currentEnchantLevel
    for tryout in range(try_count):
        tempRandom = random.random()
        # print(success_rate, tempRandom)
        # print(success_rate >= tempRandom)
        if success_rate >= tempRandom:
            _currentEnchantLevel += 1
        # 실패한 경우
        else:
            tempRandom = random.random()
            if repair_rate >= tempRandom:
                # 복구 성공 시 강화가 떨어지지 않는다.
                continue
            else:
                _currentEnchantLevel -= 1
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
    print(key, ":", result_table[key], result_table[key] * 100 / simulation_count, "%")
input()
