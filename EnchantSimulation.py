import random

try_count = 10
currentEnchantLevel = 4
success_rate = 0.3
failure_penalty = -1
lowerLimitEnchantLevel = 0

simulation_count = 1000

result_table = {}

for simulation in range(simulation_count):
    _currentEnchantLevel = currentEnchantLevel
    for tryout in range(try_count):
        if success_rate <= random.random():
            _currentEnchantLevel += 1
        else:
            _currentEnchantLevel -= 1
            if _currentEnchantLevel < lowerLimitEnchantLevel:
                _currentEnchantLevel = lowerLimitEnchantLevel
    print("result enchantLevel : ", _currentEnchantLevel)
    if _currentEnchantLevel in result_table:
        result_table[_currentEnchantLevel] = result_table[_currentEnchantLevel] + 1
    else:
        result_table[_currentEnchantLevel] = 1

sorted_keys = sorted(result_table.keys())
for key in sorted_keys:
    print(key, ":", result_table[key])
