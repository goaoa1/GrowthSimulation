class Player:
    #인벤토리
    item_List = []
    equipment_List = []
    def __init__(self):
        self.item_List = None
        self.Equipment_List = None


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
                if _expectedGrowth is not None:
                    pass
                else:
                    _expectedGrowth = None
                if equipment.isEnchantable(self):
                    _expectedGrowth = max(_expectedGrowth, equipment.calculateExpectedGrowth())
     

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
    enchantLevel = 0
    enchantType = ""
    def __init__():
        pass

    def doEnchant():
        # 성공 시 강화 단계 상승
        # 실패 시 아무일도 일어나지 않음 또는 강화 단계 하락
        pass

    def getEnchantMaterial(self.enchantLevel):
        pass

    def calculateExpectedGrowth(self,player):
        pass

    def isEnchantable(self,player):
        pass

    # 외부에서 주어진 테이블 대로
    def getBattlePoint(self.enchantLevel):
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
    gaining = (0,0)
    gaining1 = (0,0)
    gaining2 = (0,0)
    battlePointLimit = 0

    def __init__(self,tuple,tuple1,tuple2):
        self.gaining = tuple
        self.gaining1 = tuple1
        self.gaining2 = tuple2


    def isPlayerEnterable(self,player):
        return player >= self.battlePointLimit
    
    def giveItem(self,player):
        player.item_List.append(self.gaining1)

    def getPredictedGainings(self):
        return (self.gaining, self.gaining1, self.gaining2)