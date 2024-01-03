import pandas as pd

excel_file_path = "Input.xlsx"

player_df = pd.read_excel(excel_file_path, "Player")
huntingField_df = pd.read_excel(excel_file_path, "HuntingField")
enchantData_df = pd.read_excel(excel_file_path, "EnchantData")
equipmentData_df = pd.read_excel(excel_file_path, "EquipmentData")


def build_dict(dataFrame):
    rv_dict = {}

    for index, selectedRow in dataFrame.iterrows():
        key_value = selectedRow["key"]

        # key에 대한 딕셔너리가 없으면 생성
        if key_value not in rv_dict:
            rv_dict[key_value] = {}

        # 나머지 키와 값을 할당
        for col in dataFrame.columns:
            if col not in ["key"]:
                rv_dict[key_value][col] = selectedRow[col]
    return rv_dict


def build_dict_group_level(dataFrame):
    rv_dict = {}

    for index, selectedRow in dataFrame.iterrows():
        key_value = selectedRow["key"]
        level_value = selectedRow["level"]

        # key에 대한 딕셔너리가 없으면 생성
        if key_value not in rv_dict:
            rv_dict[key_value] = {}

        # level에 대한 딕셔너리가 없으면 생성
        if level_value not in rv_dict[key_value]:
            rv_dict[key_value][level_value] = {}

        # 나머지 키와 값을 할당
        for col in dataFrame.columns:
            if col == "enchantRecipe":
                temp_list = selectedRow[col].split(" ")
                result_tuple = [
                    (temp_list[i], int(temp_list[i + 1]))
                    for i in range(0, len(temp_list), 2)
                ]
                rv_dict[key_value][level_value][col] = result_tuple
            elif col not in ["key", "level"]:
                rv_dict[key_value][level_value][col] = selectedRow[col]

    return rv_dict


def build_enchantData():
    return build_dict_group_level(enchantData_df)


def build_playerData():
    return build_dict(player_df)


def build_huntingFieldData():
    return build_dict(huntingField_df)


def build_equipmentData():
    return build_dict(equipmentData_df)


class CustomDataFrame:
    dataFrame = {}

    def __init__(self):
        self.dataFrame = {}
        # TODO 매턴 데이터 누적되게
        self.dataFrame["turn"] = []
        self.dataFrame["player_key"] = []
        self.dataFrame["item0"] = []
        self.dataFrame["count0"] = []
        self.dataFrame["item1"] = []
        self.dataFrame["count1"] = []
        self.dataFrame["item2"] = []
        self.dataFrame["count2"] = []
        self.dataFrame["equipment0"] = []
        self.dataFrame["equipment0_level"] = []
        self.dataFrame["equipment1"] = []
        self.dataFrame["equipment1_level"] = []
        self.dataFrame["equipment2"] = []
        self.dataFrame["equipment2_level"] = []
        self.dataFrame["battlePoint"] = []
        self.dataFrame["huntingField"] = []

    def build_dataFrame(
        self,
        turn,
        player_key,
        item0,
        count0,
        item1,
        count1,
        item2,
        count2,
        equipment0,
        equipment0_level,
        equipment1,
        equipment1_level,
        equipment2,
        equipment2_level,
        battlePoint,
        huntingField,
    ):
        self.dataFrame["turn"].append(turn)
        self.dataFrame["player_key"].append(player_key)
        self.dataFrame["item0"].append(item0)
        self.dataFrame["count0"].append(count0)
        self.dataFrame["item1"].append(item1)
        self.dataFrame["count1"].append(count1)
        self.dataFrame["item2"].append(item2)
        self.dataFrame["count2"].append(count2)
        self.dataFrame["equipment0"].append(equipment0)
        self.dataFrame["equipment0_level"].append(equipment0_level)
        self.dataFrame["equipment1"].append(equipment1)
        self.dataFrame["equipment1_level"].append(equipment1_level)
        self.dataFrame["equipment2"].append(equipment2)
        self.dataFrame["equipment2_level"].append(equipment2_level)
        self.dataFrame["battlePoint"].append(battlePoint)
        self.dataFrame["huntingField"].append(huntingField)

    def exportToExcel(self):
        df = pd.DataFrame(self.dataFrame)

        df.to_excel("Output.xlsx", index=False, sheet_name="Output")
        return None


# print(build_enchantData())
# print(build_playerData())
