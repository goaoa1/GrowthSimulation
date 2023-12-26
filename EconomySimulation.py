from math import comb
import random
import EnchantSimulator

class Player:
    #인벤토리
    # key : count
    item_dict = {}
    equipment_List = []
    def __init__(self):
        self.item_dict = None
        self.equipment_List = None


    def chooseHuntingField(self,huntingField_List):
        # 사용 가능한 사냥터 찾기
        _enterableHuntingField_List = []
        for huntingField in huntingField_List:
            if huntingField.isPlayerEnterable(self):
                _enterableHuntingField_List.append(huntingField)

        # 그 사냥터에서 획득 가능한 재화 찾기
        for huntingField in _enterableHuntingField_List:
            huntingField.getPredictedGainings()
        # 그 사냥터에서 성장할 수 있는 기댓값 찾기(획득 가능한 재화를 획득했다고 쳤을 때 성장 기댓값 계산)
            # 강화 가능한 장비류 수집
            _expectedGrowthFromHuntingField = 0
            _expectedGrowth = None
            for equipment in self.equipment_List:
                if equipment.isEnchantable(self):
                    # 인벤토리에 존재하는 개수
                    # TODO 여기는 강화 타입이 penalty 일때를 의미
                    # TODO 플레이어 인벤토리를 읽도록 처리
                    # TODO getEnchantMaterial
                    try_Count = 10
                    __expectedGrowth = _expectedGrowth
                    # 몇 회 시도하는 게 최선인지 알 수 없으니 try_Count가 n이라면 1~n까지 시도한 경우의 수를 모두 따지고 그중 가장 큰 값을 가져가자! 
                    for _try_Count in range(try_Count):
                        _targetEnchantLevel = _try_Count
                        __expectedGrowth = max(_expectedGrowth, equipment.calculateExpectedGrowth(_try_Count,_targetEnchantLevel))
                    
                    _expectedGrowth = max(__expectedGrowth,_expectedGrowth)
                else:
                    print("해당 장비는 강화 불가능합니다.")                    
                    
     

        # 그 기댓값들의 최대값의 사냥터를 반환
        return huntingField

    def chooseEnchant(self):
        equipment = Equipment()
        return equipment

    def runEnchant(equipment):
        # 인벤토리에서 재화 차감
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

    def buyItem():
        pass

    def sellItem():
        pass


# 재화
class Item:
    def __init__():
        pass


# 장비
class Equipment:
    #TODO static... 또는 별도 데이터 테이블로 빼자
    #level : DD,PV,HP,successPercent
    # TODO failure_penalty, repair_rate
    # {"DD":0, "PV":0, "HP":0, "success_rate" : 0.1, "failure_penalty":-1, "repair_rate":0.8}
    enchantTable = {0:{"DD":0, "PV":0, "HP":0, "success_rate" : 0.1, "failure_penalty":-1, "repair_rate":0.8, "enchantMaterial":0,"enchantMaterial_count":1, "enchantMaterial1":0,"enchantMaterial_count1":1, "enchantMaterial2":0,"enchantMaterial_count2":1 }
                    , 1:{"DD":0, "PV":0, "HP":0, "success_rate" : 0.1, "failure_penalty":-1, "repair_rate":0.8 "enchantMaterial":0,"enchantMaterial_count":1, "enchantMaterial1":0,"enchantMaterial_count1":1, "enchantMaterial2":0,"enchantMaterial_count2":1 }
                     , 2:{"DD":0, "PV":0, "HP":0, "success_rate" : 0.1, "failure_penalty":-1, "repair_rate":0.8 "enchantMaterial":0,"enchantMaterial_count":1, "enchantMaterial1":0,"enchantMaterial_count1":1, "enchantMaterial2":0,"enchantMaterial_count2":1 }
                     , 3:{"DD":0, "PV":0, "HP":0, "success_rate" : 0.1, "failure_penalty":-1, "repair_rate":0.8 "enchantMaterial":0,"enchantMaterial_count":1, "enchantMaterial1":0,"enchantMaterial_count1":1, "enchantMaterial2":0,"enchantMaterial_count2":1 }}
    enchantLevel = 0
    enchantType = "penalty1"
    lowerLimitEnchantLevel = 0
    def __init__(self,enchantLevel,enchantType):
        self.enchantLevel
        self.enchantType

    def doEnchant():
        # 성공 시 강화 단계 상승
        # 실패 시 아무일도 일어나지 않음 또는 강화 단계 하락
        pass

    def getEnchantMaterial(self.enchantLevel):
        pass

    # 시행 횟수 - 강화 확률 토대로 계산
    def calculateExpectedGrowth(self,try_Count,targetEnchantLevel):
        success_Percent = self.enchantTable[targetEnchantLevel-1]
        _expectedGrowth = 0
        # 강화 결과 성공 시(양수가 나오는) 기대 성장치 합계
        # TODO 강화 성공 한계 치 등록 필요
        for _targetEnchantLevel in range(targetEnchantLevel):
            _expectedGrowth = _expectedGrowth + self.enchantTable[_targetEnchantLevel] * Calculator.calculateTargetEnchantLevelSuccessPercent(self.enchantType,try_Count,_targetEnchantLevel,success_Percent) - self.enchantTable[self.enchantLevel]
        # 강화 결과 실패 시(음수가 나오는) 기대 성장치 합계
        # TODO 강화 실패 한계 치 등록 필요
        for _targetEnchantLevel in range(targetEnchantLevel):
            # success_Percent를 1의 보수로 바꿨다.
            _expectedGrowth = _expectedGrowth + self.enchantTable[_targetEnchantLevel] * Calculator.calculateTargetEnchantLevelSuccessPercent(self.enchantType,try_Count,_targetEnchantLevel,1-success_Percent) - self.enchantTable[self.enchantLevel]
        return _expectedGrowth
             




    def isEnchantable(self,player):
        pass

    # 외부에서 주어진 테이블 대로
    def getBattlePoint(self.enchantLevel):
        pass

class Calculator:
    pass


class SimulationManager:
    currentTurn = 0
    player_List = None
    huntingField_List = []

    def __init__(self):
        _huntingField = HuntingField((0,10),(1,13),(2,20))
        _huntingField1 = HuntingField((0,10),(1,13),(2,20))
        _huntingField2 = HuntingField((0,10),(1,13),(2,20))
        self.huntingField_List.append(_huntingField,_huntingField1,_huntingField2)
        self.player_List = Player()

    def processTurn(self):
        # n회 루프하도록 한다.
        for player in self.player_List:
            player.chooseHuntingField().giveItem(player)
            player.runEnchant(player.chooseEnchant())
            print(player.getBattlePoint())


class HuntingField:
    # item, count
    gaining_list = [(0,0),(0,0),(0,0)]
    battlePointLimit = 0

    def __init__(self,tuple,tuple1,tuple2):
        self.gaining = tuple
        self.gaining1 = tuple1
        self.gaining2 = tuple2


    def isPlayerEnterable(self,player):
        return player >= self.battlePointLimit
    
    def giveItem(self,player):
        for gaining in self.gaining_list:
            player.acquire_item(gaining)

    def getPredictedGainings(self):
        return (self.gaining, self.gaining1, self.gaining2)