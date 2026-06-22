"""
完整材料参数数据库 — 综合5份行业资料
涵盖: 正极/负极/导电剂/粘结剂/隔膜/电解液/壳体/辅件 全部物性参数
"""

# ═══════════════════════════════════════════
#  正极材料
# ═══════════════════════════════════════════
POSITIVE_MATERIALS = {
    "NCA": {
        "name": "NCA (LiNiCoAlO2)", "reversible_capacity_mAh_g": 192,
        "charge_capacity_mAh_g": 208.7, "first_efficiency": 0.92,
        "true_density_g_cm3": 4.65, "active_fraction": 0.95,
        "pressed_density_g_cm3": 3.59, "voltage_V": 3.65,
        "ad_range_mg_cm2": (16, 20), "scenario": "超高能量 (Tesla/Panasonic)",
    },
    "NCM811": {
        "name": "NCM811", "reversible_capacity_mAh_g": 182,
        "charge_capacity_mAh_g": 191.6, "first_efficiency": 0.95,
        "true_density_g_cm3": 4.65, "active_fraction": 0.95,
        "pressed_density_g_cm3": 3.45, "voltage_V": 3.65,
        "ad_range_mg_cm2": (16, 20), "scenario": "高镍能量型",
    },
    "NCM622": {
        "name": "NCM622", "reversible_capacity_mAh_g": 180,
        "charge_capacity_mAh_g": 189.5, "first_efficiency": 0.95,
        "true_density_g_cm3": 4.65, "active_fraction": 0.94,
        "pressed_density_g_cm3": 3.5, "voltage_V": 3.65,
        "ad_range_mg_cm2": (17, 21), "scenario": "中高镍平衡型",
    },
    "NCM523": {
        "name": "NCM523", "reversible_capacity_mAh_g": 160,
        "charge_capacity_mAh_g": 168.4, "first_efficiency": 0.95,
        "true_density_g_cm3": 4.65, "active_fraction": 0.94,
        "pressed_density_g_cm3": 3.5, "voltage_V": 3.60,
        "ad_range_mg_cm2": (18, 22), "scenario": "消费级能量型",
    },
    "LCO": {
        "name": "LCO (LiCoO2)", "reversible_capacity_mAh_g": 150,
        "charge_capacity_mAh_g": 157.9, "first_efficiency": 0.95,
        "true_density_g_cm3": 5.05, "active_fraction": 0.95,
        "pressed_density_g_cm3": 3.9, "voltage_V": 3.80,
        "ad_range_mg_cm2": (19, 23), "scenario": "消费级高电压型",
    },
    "LFP": {
        "name": "LFP (LiFePO4)", "reversible_capacity_mAh_g": 140,
        "charge_capacity_mAh_g": 147.4, "first_efficiency": 0.95,
        "true_density_g_cm3": 3.65, "active_fraction": 0.93,
        "pressed_density_g_cm3": 3.3, "voltage_V": 3.20,
        "ad_range_mg_cm2": (20, 24), "scenario": "动力/储能型",
    },
    "LMFP": {
        "name": "LMFP (LiMnFePO4)", "reversible_capacity_mAh_g": 150,
        "charge_capacity_mAh_g": 157.9, "first_efficiency": 0.95,
        "true_density_g_cm3": 3.5, "active_fraction": 0.93,
        "pressed_density_g_cm3": 2.6, "voltage_V": 3.55,
        "ad_range_mg_cm2": (18, 22), "scenario": "中高能量+高安全",
    },
}

# ═══════════════════════════════════════════
#  负极材料
# ═══════════════════════════════════════════
NEGATIVE_MATERIALS = {
    "天然石墨": {
        "name": "天然石墨", "reversible_capacity_mAh_g": 350,
        "charge_capacity_mAh_g": 380.4, "first_efficiency": 0.92,
        "true_density_g_cm3": 2.2, "active_fraction": 0.95,
        "pressed_density_g_cm3": 1.6, "voltage_V": 0.10,
        "ad_range_mg_cm2": (10, 13), "expansion_rate": 0.0,
        "scenario": "消费级能量型",
    },
    "人造石墨": {
        "name": "人造石墨", "reversible_capacity_mAh_g": 320,
        "charge_capacity_mAh_g": 347.8, "first_efficiency": 0.92,
        "true_density_g_cm3": 2.2, "active_fraction": 0.95,
        "pressed_density_g_cm3": 1.6, "voltage_V": 0.10,
        "ad_range_mg_cm2": (10, 12), "expansion_rate": 0.0,
        "scenario": "动力/循环型",
    },
    "石墨+Si (96.5/3.5)": {
        "name": "石墨+Si (96.5/3.5)", "reversible_capacity_mAh_g": 399.9,
        "charge_capacity_mAh_g": 444.3, "first_efficiency": 0.90,
        "true_density_g_cm3": 2.2, "active_fraction": 0.95,
        "pressed_density_g_cm3": 1.494, "voltage_V": 0.12,
        "ad_range_mg_cm2": (10, 12), "expansion_rate": 0.008,
        "scenario": "高容量型 (Tesla 4680)",
    },
    "硅碳 (SiC)": {
        "name": "硅碳 SiC", "reversible_capacity_mAh_g": 450,
        "charge_capacity_mAh_g": 500.0, "first_efficiency": 0.87,
        "true_density_g_cm3": 2.3, "active_fraction": 0.92,
        "pressed_density_g_cm3": 1.55, "voltage_V": 0.15,
        "ad_range_mg_cm2": (8, 10), "expansion_rate": 0.02,
        "scenario": "高容量型 (5% Si)",
    },
    "硅氧 (SiOx)": {
        "name": "硅氧 SiOx", "reversible_capacity_mAh_g": 450,
        "charge_capacity_mAh_g": 529.4, "first_efficiency": 0.85,
        "true_density_g_cm3": 2.2, "active_fraction": 0.90,
        "pressed_density_g_cm3": 1.5, "voltage_V": 0.17,
        "ad_range_mg_cm2": (8, 10), "expansion_rate": 0.015,
        "scenario": "高容量型 (膨胀<SiC)",
    },
    "软碳": {
        "name": "软碳", "reversible_capacity_mAh_g": 300,
        "charge_capacity_mAh_g": 333.3, "first_efficiency": 0.88,
        "true_density_g_cm3": 2.0, "active_fraction": 0.94,
        "pressed_density_g_cm3": 1.45, "voltage_V": 0.15,
        "ad_range_mg_cm2": (9, 11), "expansion_rate": 0.0,
        "scenario": "快充型",
    },
}

# ═══════════════════════════════════════════
#  导电剂 / 粘结剂 / 辅料 真密度
# ═══════════════════════════════════════════
ADDITIVE_DENSITY = {
    "SP": 2.05,        # Super P 导电炭黑
    "CNTs": 1.31,       # 碳纳米管
    "PVdF": 1.77,       # 聚偏氟乙烯 (正极粘结剂)
    "CMC": 1.28,        # 羧甲基纤维素钠 (负极增稠剂)
    "SBR": 1.0,         # 丁苯橡胶 (负极粘结剂)
    "PAA": 1.0,         # 聚丙烯酸
}

# ═══════════════════════════════════════════
#  集流体 / 隔膜 / 电解液 / 壳体
# ═══════════════════════════════════════════
COMPONENT_DB = {
    "Al_foil": {"density_g_cm3": 2.73, "thickness_options_um": [10, 12, 15, 16, 20]},
    "Cu_foil": {"density_g_cm3": 8.46, "thickness_options_um": [6, 8, 10, 12]},
    "separator_PE": {"density_g_cm3": 1.0, "porosity": 0.49, "thickness_options_um": [9, 10, 12, 16, 20, 25]},
    "electrolyte": {"density_g_cm3": 1.22, "injection_factor": 1.37},
    "steel_case": {"density_g_cm3": 8.07, "areal_density_mg_cm2": 2.42},
    "insulator_PP": {"areal_density_mg_cm2": 0.446},  # 219µm PP film
    "insulator_neg": {"areal_density_mg_cm2": 0.159},  # 329µm
    "cap_assembly": {"areal_density_mg_cm2": 2.53},    # 顶盖组件
}

# ═══════════════════════════════════════════
#  电芯规格
# ═══════════════════════════════════════════
CELL_SPECS = {
    "18650": {"outer_D": 18.0, "H": 65.0, "inner_D": 17.4, "core_max_D": 17.0,
              "case_t_mm": 0.30, "width_range": (56, 58), "mandrel_range": (3.0, 3.5),
              "tab_pos_t_um": 165, "tab_neg_t_um": 115, "cap_t_mm": 0.9},
    "21700": {"outer_D": 21.0, "H": 70.0, "inner_D": 20.4, "core_max_D": 20.0,
              "case_t_mm": 0.30, "width_range": (60, 62), "mandrel_range": (3.5, 4.0),
              "tab_pos_t_um": 165, "tab_neg_t_um": 115, "cap_t_mm": 0.9},
    "33140": {"outer_D": 33.0, "H": 140.0, "inner_D": 32.2, "core_max_D": 31.8,
              "case_t_mm": 0.40, "width_range": (125, 132), "mandrel_range": (5.0, 6.0),
              "tab_pos_t_um": 200, "tab_neg_t_um": 150, "cap_t_mm": 1.2},
    "4680":  {"outer_D": 46.0, "H": 80.0, "inner_D": 45.04, "core_max_D": 44.7,
              "case_t_mm": 0.48, "width_range": (70, 75), "mandrel_range": (5.0, 6.0),
              "tab_pos_t_um": 400, "tab_neg_t_um": 260, "cap_t_mm": 1.5},
}


def blend_material(mat1: dict, mat2: dict, ratio1: float) -> dict:
    """混合两种材料 (加权平均所有属性)"""
    r1, r2 = ratio1, 1 - ratio1
    result = {}
    for key in mat1:
        v1, v2 = mat1[key], mat2[key]
        if isinstance(v1, (int, float)):
            result[key] = v1 * r1 + v2 * r2
        elif isinstance(v1, tuple) and len(v1) == 2:
            result[key] = (v1[0] * r1 + v2[0] * r2, v1[1] * r1 + v2[1] * r2)
        else:
            result[key] = v1  # keep string fields from primary
    return result
