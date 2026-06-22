"""
圆柱锂电池全参数设计计算引擎 v4.0
综合 5 份行业设计资料, 覆盖电芯全部物理参数
"""

import math
from dataclasses import dataclass, field


@dataclass
class DesignInput:
    """完整设计输入"""
    # 基本
    cell_type: str = "18650"
    target_capacity_mAh: float = 3000

    # 正极
    pos_material: str = "NCM523"
    pos_reversible_capacity_mAh_g: float = 160
    pos_charge_capacity_mAh_g: float = 168.4
    pos_first_efficiency: float = 0.95
    pos_true_density_g_cm3: float = 4.65
    pos_active_fraction: float = 0.94
    pos_SP_fraction: float = 0.02
    pos_CNT_fraction: float = 0.0
    pos_binder_fraction: float = 0.03
    pos_coating_ad_mg_cm2: float = 20.0
    pos_pressed_density_g_cm3: float = 3.5
    pos_foil_thickness_um: float = 15.0
    pos_width_mm: float = 57.0
    pos_coating_expansion: float = 0.0

    # 负极
    neg_material: str = "天然石墨"
    neg_reversible_capacity_mAh_g: float = 350
    neg_charge_capacity_mAh_g: float = 380.4
    neg_first_efficiency: float = 0.92
    neg_true_density_g_cm3: float = 2.2
    neg_active_fraction: float = 0.95
    neg_SP_fraction: float = 0.01
    neg_CNT_fraction: float = 0.0
    neg_CMC_fraction: float = 0.015
    neg_binder_fraction: float = 0.025
    neg_coating_ad_mg_cm2: float = 11.0
    neg_pressed_density_g_cm3: float = 1.65
    neg_foil_thickness_um: float = 8.0
    neg_width_extra_mm: float = 2.0
    neg_coating_expansion: float = 0.01

    # N/P
    np_ratio_target: float = 1.10

    # 隔膜
    separator_thickness_um: float = 16.0
    separator_porosity: float = 0.49
    separator_width_extra_mm: float = 2.0
    separator_pre_wind_n1: int = 2   # 隔膜先卷圈数
    separator_post_wind_n2: int = 2  # 隔膜后卷圈数

    # 卷绕
    mandrel_diameter_mm: float = 3.2
    neg_length_extra_mm: float = 30.0
    core_clearance_mm: float = 0.4     # 卷芯-壳体内径间隙

    # 电解液
    electrolyte_density_g_cm3: float = 1.22
    electrolyte_injection_factor: float = 1.20

    # 箔材延展率
    al_foil_elongation: float = 0.005
    cu_foil_elongation: float = 0.0
    coating_springback: float = 0.01   # 辊压回弹率


@dataclass
class FullCellResult:
    """电芯全参数计算结果"""
    # === 正极 ===
    pos_coating_true_density_g_cm3: float = 0.0
    pos_coating_pressed_density_g_cm3: float = 0.0
    pos_coating_porosity: float = 0.0
    pos_coating_thickness_target_um: float = 0.0
    pos_coating_thickness_actual_um: float = 0.0
    pos_total_thickness_um: float = 0.0
    pos_areal_capacity_mAh_cm2: float = 0.0
    pos_coating_area_cm2: float = 0.0
    pos_coating_length_mm: float = 0.0
    pos_total_length_mm: float = 0.0
    pos_coating_weight_g: float = 0.0
    pos_active_weight_g: float = 0.0
    pos_SP_weight_g: float = 0.0
    pos_binder_weight_g: float = 0.0
    pos_foil_weight_g: float = 0.0
    pos_total_weight_g: float = 0.0
    pos_coating_volume_cm3: float = 0.0
    pos_pore_volume_cm3: float = 0.0
    pos_capacity_mAh: float = 0.0

    # === 负极 ===
    neg_coating_true_density_g_cm3: float = 0.0
    neg_coating_pressed_density_g_cm3: float = 0.0
    neg_coating_porosity: float = 0.0
    neg_coating_thickness_target_um: float = 0.0
    neg_coating_thickness_actual_um: float = 0.0
    neg_total_thickness_um: float = 0.0
    neg_areal_capacity_mAh_cm2: float = 0.0
    neg_width_mm: float = 0.0
    neg_coating_area_cm2: float = 0.0
    neg_coating_length_mm: float = 0.0
    neg_total_length_mm: float = 0.0
    neg_coating_weight_g: float = 0.0
    neg_active_weight_g: float = 0.0
    neg_SP_weight_g: float = 0.0
    neg_CMC_weight_g: float = 0.0
    neg_binder_weight_g: float = 0.0
    neg_foil_weight_g: float = 0.0
    neg_total_weight_g: float = 0.0
    neg_coating_volume_cm3: float = 0.0
    neg_pore_volume_cm3: float = 0.0
    neg_capacity_mAh: float = 0.0
    actual_np_ratio: float = 0.0
    areal_np_ratio: float = 0.0

    # === 隔膜 ===
    separator_width_mm: float = 0.0
    separator_total_length_mm: float = 0.0
    separator_volume_cm3: float = 0.0
    separator_pore_volume_cm3: float = 0.0
    separator_weight_g: float = 0.0

    # === 卷绕 ===
    unit_thickness_um: float = 0.0
    unit_thickness_mm: float = 0.0
    spiral_parameter_a_um: float = 0.0
    total_winding_layers: int = 0
    positive_winding_turns: int = 0
    negative_winding_turns: int = 0
    separator_winding_turns: int = 0
    core_diameter_mm: float = 0.0
    core_diameter_soc100_mm: float = 0.0
    diameter_margin_mm: float = 0.0
    total_spiral_length_mm: float = 0.0
    core_volume_cm3: float = 0.0

    # === 电解液 ===
    total_pore_volume_cm3: float = 0.0
    electrolyte_volume_cm3: float = 0.0
    electrolyte_weight_g: float = 0.0

    # === 壳体+辅件 ===
    case_weight_g: float = 0.0
    insulator_pos_weight_g: float = 0.0
    insulator_neg_weight_g: float = 0.0
    tab_pos_weight_g: float = 0.0
    tab_neg_weight_g: float = 0.0
    cap_weight_g: float = 0.0

    # === 汇总 ===
    core_weight_g: float = 0.0
    total_cell_weight_g: float = 0.0
    cell_volume_cm3: float = 0.0
    cell_energy_Wh: float = 0.0
    gravimetric_energy_Wh_kg: float = 0.0
    volumetric_energy_Wh_L: float = 0.0
    nominal_voltage_V: float = 3.65

    # === 校核 ===
    is_core_fit: bool = True
    is_np_safe: bool = True
    warnings: list[str] = field(default_factory=list)


def _coating_true_density(active_d: float, active_f: float, sp_f: float, cnt_f: float,
                          binder_f: float, sp_d: float = 2.05, cnt_d: float = 1.31,
                          binder_d: float = 1.77) -> float:
    """涂层平均真密度 (体积加权倒数)"""
    denom = (active_f / active_d + sp_f / sp_d + cnt_f / cnt_d + binder_f / binder_d)
    return 1.0 / denom if denom > 0 else active_d


def _neg_coating_true_density(active_d: float, active_f: float, sp_f: float, cnt_f: float,
                               cmc_f: float, binder_f: float) -> float:
    """负极涂层平均真密度 (含CMC和SBR)"""
    denom = (active_f / active_d + sp_f / 2.05 + cnt_f / 1.31 + cmc_f / 1.28 + binder_f / 1.0)
    return 1.0 / denom if denom > 0 else active_d


def run_full_cell_design(inp: DesignInput) -> FullCellResult:
    r = FullCellResult(); w = []
    spec = __import__('core.material_db', fromlist=['CELL_SPECS']).CELL_SPECS[inp.cell_type]

    # ═══════════════════════════════════════
    #  正极
    # ═══════════════════════════════════════
    r.pos_coating_true_density_g_cm3 = _coating_true_density(
        inp.pos_true_density_g_cm3, inp.pos_active_fraction,
        inp.pos_SP_fraction, inp.pos_CNT_fraction, inp.pos_binder_fraction)
    r.pos_coating_pressed_density_g_cm3 = inp.pos_pressed_density_g_cm3
    r.pos_coating_porosity = 1 - r.pos_coating_pressed_density_g_cm3 / r.pos_coating_true_density_g_cm3
    r.pos_coating_thickness_target_um = inp.pos_coating_ad_mg_cm2 * 10 / inp.pos_pressed_density_g_cm3
    r.pos_coating_thickness_actual_um = r.pos_coating_thickness_target_um * (1 + inp.coating_springback)
    al_foil_t = inp.pos_foil_thickness_um * (1 - inp.al_foil_elongation)
    r.pos_total_thickness_um = 2 * r.pos_coating_thickness_actual_um + al_foil_t
    r.pos_areal_capacity_mAh_cm2 = (2 * inp.pos_coating_ad_mg_cm2 * inp.pos_active_fraction
                                     * inp.pos_reversible_capacity_mAh_g / 1000)

    denom_pos = (2 * inp.pos_coating_ad_mg_cm2 * inp.pos_active_fraction * inp.pos_reversible_capacity_mAh_g)
    r.pos_coating_area_cm2 = inp.target_capacity_mAh * 1000 / denom_pos
    r.pos_coating_length_mm = r.pos_coating_area_cm2 / (inp.pos_width_mm / 10) * 10
    r.pos_total_length_mm = r.pos_coating_length_mm

    r.pos_coating_weight_g = (r.pos_coating_area_cm2 * 2 * inp.pos_coating_ad_mg_cm2 / 1000)
    r.pos_active_weight_g = r.pos_coating_weight_g * inp.pos_active_fraction
    r.pos_SP_weight_g = r.pos_coating_weight_g * inp.pos_SP_fraction
    r.pos_binder_weight_g = r.pos_coating_weight_g * inp.pos_binder_fraction
    al_areal = al_foil_t / 10000 * 2.73  # g/cm²
    r.pos_foil_weight_g = r.pos_coating_area_cm2 * 2 * al_areal
    r.pos_total_weight_g = r.pos_coating_weight_g + r.pos_foil_weight_g
    r.pos_coating_volume_cm3 = r.pos_coating_weight_g / r.pos_coating_true_density_g_cm3
    r.pos_pore_volume_cm3 = r.pos_coating_volume_cm3 * r.pos_coating_porosity
    r.pos_capacity_mAh = r.pos_active_weight_g * inp.pos_reversible_capacity_mAh_g

    # ═══════════════════════════════════════
    #  负极
    # ═══════════════════════════════════════
    r.neg_coating_true_density_g_cm3 = _neg_coating_true_density(
        inp.neg_true_density_g_cm3, inp.neg_active_fraction,
        inp.neg_SP_fraction, inp.neg_CNT_fraction, inp.neg_CMC_fraction, inp.neg_binder_fraction)
    r.neg_coating_pressed_density_g_cm3 = inp.neg_pressed_density_g_cm3
    r.neg_coating_porosity = 1 - r.neg_coating_pressed_density_g_cm3 / r.neg_coating_true_density_g_cm3
    r.neg_coating_thickness_target_um = inp.neg_coating_ad_mg_cm2 * 10 / inp.neg_pressed_density_g_cm3
    r.neg_coating_thickness_actual_um = r.neg_coating_thickness_target_um * (1 + inp.coating_springback)
    cu_foil_t = inp.neg_foil_thickness_um * (1 - inp.cu_foil_elongation)
    r.neg_total_thickness_um = 2 * r.neg_coating_thickness_actual_um + cu_foil_t
    r.neg_areal_capacity_mAh_cm2 = (2 * inp.neg_coating_ad_mg_cm2 * inp.neg_active_fraction
                                     * inp.neg_reversible_capacity_mAh_g / 1000)

    r.neg_width_mm = inp.pos_width_mm + inp.neg_width_extra_mm
    r.neg_coating_length_mm = r.pos_coating_length_mm + inp.neg_length_extra_mm
    r.neg_total_length_mm = r.neg_coating_length_mm
    r.neg_coating_area_cm2 = (r.neg_coating_length_mm / 10) * (r.neg_width_mm / 10)

    r.neg_coating_weight_g = r.neg_coating_area_cm2 * 2 * inp.neg_coating_ad_mg_cm2 / 1000
    r.neg_active_weight_g = r.neg_coating_weight_g * inp.neg_active_fraction
    r.neg_SP_weight_g = r.neg_coating_weight_g * inp.neg_SP_fraction
    r.neg_CMC_weight_g = r.neg_coating_weight_g * inp.neg_CMC_fraction
    r.neg_binder_weight_g = r.neg_coating_weight_g * inp.neg_binder_fraction
    cu_areal = cu_foil_t / 10000 * 8.46
    r.neg_foil_weight_g = r.neg_coating_area_cm2 * 2 * cu_areal
    r.neg_total_weight_g = r.neg_coating_weight_g + r.neg_foil_weight_g
    r.neg_coating_volume_cm3 = r.neg_coating_weight_g / r.neg_coating_true_density_g_cm3
    r.neg_pore_volume_cm3 = r.neg_coating_volume_cm3 * r.neg_coating_porosity
    r.neg_capacity_mAh = r.neg_active_weight_g * inp.neg_reversible_capacity_mAh_g
    r.actual_np_ratio = r.neg_capacity_mAh / r.pos_capacity_mAh if r.pos_capacity_mAh > 0 else 0
    r.areal_np_ratio = r.neg_areal_capacity_mAh_cm2 / r.pos_areal_capacity_mAh_cm2 if r.pos_areal_capacity_mAh_cm2 > 0 else 0

    if r.actual_np_ratio < 1.05:
        w.append(f"N/P={r.actual_np_ratio:.3f} < 1.05 析锂风险!"); r.is_np_safe = False
    elif r.actual_np_ratio < 1.08:
        w.append(f"N/P={r.actual_np_ratio:.3f} 偏低"); r.is_np_safe = True
    else:
        r.is_np_safe = True

    # ═══════════════════════════════════════
    #  隔膜
    # ═══════════════════════════════════════
    r.separator_width_mm = r.neg_width_mm + inp.separator_width_extra_mm
    r.separator_total_length_mm = (r.pos_coating_length_mm
                                    + (inp.separator_pre_wind_n1 + inp.separator_post_wind_n2)
                                    * math.pi * inp.mandrel_diameter_mm * 1.2)
    sep_area = (r.separator_total_length_mm / 10) * (r.separator_width_mm / 10)
    r.separator_volume_cm3 = sep_area * 2 * inp.separator_thickness_um / 10000
    r.separator_pore_volume_cm3 = r.separator_volume_cm3 * inp.separator_porosity
    r.separator_weight_g = r.separator_volume_cm3 * 1.0  # PE density

    # ═══════════════════════════════════════
    #  卷绕几何 (阿基米德螺线)
    # ═══════════════════════════════════════
    r.unit_thickness_um = r.pos_total_thickness_um + r.neg_total_thickness_um + 2 * inp.separator_thickness_um
    r.unit_thickness_mm = r.unit_thickness_um / 1000
    r.spiral_parameter_a_um = r.unit_thickness_um / (2 * math.pi)

    core_max_D = spec["core_max_D"]
    mandrel_r = inp.mandrel_diameter_mm / 2
    if r.unit_thickness_mm > 0:
        r.total_winding_layers = int((core_max_D / 2 - mandrel_r) / r.unit_thickness_mm)
    else:
        r.total_winding_layers = 0

    # 正极圈数 = 总圈数 - 内部隔膜/负极提前圈数
    pre_turns = inp.separator_pre_wind_n1  # 隔膜先卷
    r.positive_winding_turns = max(0, r.total_winding_layers - pre_turns)
    r.negative_winding_turns = r.positive_winding_turns + 1  # 负极多1圈尾包
    r.separator_winding_turns = r.positive_winding_turns + pre_turns + inp.separator_post_wind_n2

    # 阿基米德螺线: r(θ) = a + b·θ,  b = T_unit/(2π)
    # L = ∫₀^(2πN) √((a+bθ)² + b²) dθ
    a_mm = mandrel_r
    b_mm = r.unit_thickness_mm / (2 * math.pi)
    theta_max = 2 * math.pi * r.positive_winding_turns
    # 数值积分
    n_pts = max(1000, r.positive_winding_turns * 100)
    dtheta = theta_max / n_pts
    total_L = 0.0
    for i in range(n_pts):
        th = (i + 0.5) * dtheta
        rr = a_mm + b_mm * th
        total_L += math.sqrt(rr * rr + b_mm * b_mm) * dtheta
    r.total_spiral_length_mm = total_L

    r.core_diameter_mm = mandrel_r * 2 + 2 * r.unit_thickness_mm * r.total_winding_layers

    # SOC100%膨胀后直径
    pos_t_soc100 = r.pos_total_thickness_um * (1 + inp.pos_coating_expansion)
    neg_t_soc100 = r.neg_total_thickness_um * (1 + inp.neg_coating_expansion)
    unit_soc100 = pos_t_soc100 + neg_t_soc100 + 2 * inp.separator_thickness_um
    r.core_diameter_soc100_mm = mandrel_r * 2 + 2 * (unit_soc100 / 1000) * r.total_winding_layers

    r.diameter_margin_mm = core_max_D - r.core_diameter_soc100_mm
    if r.diameter_margin_mm < 0:
        w.append(f"SOC100%卷芯({r.core_diameter_soc100_mm:.2f}mm)超限({core_max_D}mm)!")
        r.is_core_fit = False
    elif r.diameter_margin_mm < 0.3:
        w.append(f"膨胀后裕量仅{r.diameter_margin_mm:.2f}mm")
        r.is_core_fit = True
    else:
        r.is_core_fit = True

    core_H = inp.pos_width_mm + 3  # 箔材折叠3mm
    r.core_volume_cm3 = math.pi * (r.core_diameter_mm / 2)**2 * core_H / 1000

    # ═══════════════════════════════════════
    #  电解液
    # ═══════════════════════════════════════
    r.total_pore_volume_cm3 = r.pos_pore_volume_cm3 + r.neg_pore_volume_cm3 + r.separator_pore_volume_cm3
    r.electrolyte_volume_cm3 = r.total_pore_volume_cm3 * inp.electrolyte_injection_factor
    r.electrolyte_weight_g = r.electrolyte_volume_cm3 * inp.electrolyte_density_g_cm3

    # ═══════════════════════════════════════
    #  壳体 + 辅件
    # ═══════════════════════════════════════
    case_area = math.pi * spec["outer_D"] / 10 * spec["H"] / 10  # cm²
    r.case_weight_g = case_area * 0.20  # g/cm² steel (~7.4g for 18650)
    # 绝缘片
    inset_D = spec["inner_D"]
    r.insulator_pos_weight_g = math.pi * (inset_D / 20)**2 * 0.0446
    r.insulator_neg_weight_g = math.pi * (inset_D / 20)**2 * 0.0159
    # 极耳 (简化: 厚度×宽度×长度, 18650典型Al:165µm×4mm×50mm→0.089g)
    tab_w_mm = 4.0  # typical tab width
    r.tab_pos_weight_g = spec["tab_pos_t_um"] / 1000 * tab_w_mm / 10 * 50 / 10 * 2.7 / 10
    r.tab_neg_weight_g = spec["tab_neg_t_um"] / 1000 * tab_w_mm / 10 * 50 / 10 * 8.9 / 10
    # 顶盖
    cap_area = math.pi * (inset_D / 20)**2
    r.cap_weight_g = cap_area * 0.253  # g/cm²

    # ═══════════════════════════════════════
    #  汇总
    # ═══════════════════════════════════════
    r.core_weight_g = (r.pos_total_weight_g + r.neg_total_weight_g +
                       r.separator_weight_g + r.electrolyte_weight_g)
    r.total_cell_weight_g = (r.core_weight_g + r.case_weight_g + r.insulator_pos_weight_g +
                              r.insulator_neg_weight_g + r.tab_pos_weight_g +
                              r.tab_neg_weight_g + r.cap_weight_g)
    r.cell_volume_cm3 = math.pi * (spec["outer_D"] / 20)**2 * spec["H"] / 10
    r.nominal_voltage_V = 3.65
    r.cell_energy_Wh = inp.target_capacity_mAh / 1000 * r.nominal_voltage_V
    r.gravimetric_energy_Wh_kg = (r.cell_energy_Wh / r.total_cell_weight_g * 1000
                                   if r.total_cell_weight_g > 0 else 0)
    r.volumetric_energy_Wh_L = r.cell_energy_Wh / r.cell_volume_cm3 * 1000

    r.warnings = w
    return r
