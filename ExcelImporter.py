import pandas as pd

excel_file_path = "input.xlsx"

player_df = pd.read_excel(excel_file_path, "Player")
huntingField_df = pd.read_excel(excel_file_path, "HuntingField")
enchantData_df = pd.read_excel(excel_file_path, "EnchantData")


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


# print(build_enchantData())
# print(build_playerData())
