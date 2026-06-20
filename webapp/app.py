"""网页版电芯设计 — 直接调用 PC 版 core/ 计算引擎, 100% 一致"""
import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from flask import Flask, render_template, request, jsonify
from core.electrode_calc import DesignInput, run_full_cell_design
from core.material_db import POSITIVE_MATERIALS, NEGATIVE_MATERIALS, CELL_SPECS

def _fix_tuples(d):
    """Recursively convert tuples to lists for JSON serialization"""
    if isinstance(d, dict):
        return {k: _fix_tuples(v) for k, v in d.items()}
    if isinstance(d, (list, tuple)):
        return [_fix_tuples(v) for v in d]
    return d

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
        pos_mats=list(POSITIVE_MATERIALS.keys()),
        neg_mats=list(NEGATIVE_MATERIALS.keys()),
        cells=list(CELL_SPECS.keys()),
        cells_json=json.dumps(_fix_tuples(CELL_SPECS)),
        pos_json=json.dumps(_fix_tuples(POSITIVE_MATERIALS)),
        neg_json=json.dumps(_fix_tuples(NEGATIVE_MATERIALS)))

@app.route('/materials/<mtype>')
def get_materials(mtype):
    if mtype == 'positive': return jsonify(POSITIVE_MATERIALS)
    if mtype == 'negative': return jsonify(NEGATIVE_MATERIALS)
    return jsonify({})

@app.route('/cells/<name>')
def get_cell(name):
    if name in CELL_SPECS: return jsonify(CELL_SPECS[name])
    return jsonify({})

@app.route('/calc', methods=['POST'])
def calc():
    try:
        data = request.get_json()
        inp = DesignInput()
        inp.cell_type = data.get('cell_type', '18650')
        inp.target_capacity_mAh = float(data.get('target_cap', 3000))

        # Positive
        inp.pos_reversible_capacity_mAh_g = float(data.get('pos_rev_cap', 182))
        inp.pos_active_fraction = float(data.get('pos_act_f', 0.95))
        inp.pos_coating_ad_mg_cm2 = float(data.get('pos_ad', 20))
        inp.pos_pressed_density_g_cm3 = float(data.get('pos_pd', 3.45))
        inp.pos_foil_thickness_um = float(data.get('pos_foil', 15))
        inp.pos_width_mm = float(data.get('pos_width', 57))
        inp.pos_coating_expansion = float(data.get('pos_exp', 0))

        # Negative
        inp.neg_reversible_capacity_mAh_g = float(data.get('neg_rev_cap', 350))
        inp.neg_active_fraction = float(data.get('neg_act_f', 0.95))
        inp.neg_coating_ad_mg_cm2 = float(data.get('neg_ad', 11))
        inp.neg_pressed_density_g_cm3 = float(data.get('neg_pd', 1.65))
        inp.neg_foil_thickness_um = float(data.get('neg_foil', 8))
        inp.neg_width_extra_mm = float(data.get('neg_wextra', 2))
        inp.neg_coating_expansion = float(data.get('neg_exp', 0.01))

        # Separator, winding, electrolyte
        inp.separator_thickness_um = float(data.get('sep_t', 16))
        inp.separator_porosity = float(data.get('sep_por', 0.49))
        inp.mandrel_diameter_mm = float(data.get('mandrel', 3.2))
        inp.electrolyte_density_g_cm3 = float(data.get('elyte_d', 1.22))
        inp.electrolyte_injection_factor = float(data.get('elyte_f', 1.20))
        inp.np_ratio_target = float(data.get('np_target', 1.10))

        r = run_full_cell_design(inp)
        return jsonify({
            'success': True,
            'cell_type': inp.cell_type,
            'target_capacity_mAh': inp.target_capacity_mAh,
            'pos_coating_length_mm': round(r.pos_coating_length_mm, 1),
            'pos_total_thickness_um': round(r.pos_total_thickness_um, 1),
            'pos_coating_thickness_actual_um': round(r.pos_coating_thickness_actual_um, 1),
            'pos_coating_true_density_g_cm3': round(r.pos_coating_true_density_g_cm3, 4),
            'pos_coating_pressed_density_g_cm3': round(r.pos_coating_pressed_density_g_cm3, 2),
            'pos_coating_porosity': round(r.pos_coating_porosity * 100, 1),
            'pos_areal_capacity_mAh_cm2': round(r.pos_areal_capacity_mAh_cm2, 4),
            'pos_coating_area_cm2': round(r.pos_coating_area_cm2, 1),
            'pos_active_weight_g': round(r.pos_active_weight_g, 2),
            'pos_coating_weight_g': round(r.pos_coating_weight_g, 2),
            'pos_foil_weight_g': round(r.pos_foil_weight_g, 2),
            'pos_total_weight_g': round(r.pos_total_weight_g, 2),
            'pos_coating_volume_cm3': round(r.pos_coating_volume_cm3, 4),
            'pos_pore_volume_cm3': round(r.pos_pore_volume_cm3, 4),
            'pos_capacity_mAh': round(r.pos_capacity_mAh, 1),
            'neg_coating_length_mm': round(r.neg_coating_length_mm, 1),
            'neg_width_mm': round(r.neg_width_mm, 1),
            'neg_total_thickness_um': round(r.neg_total_thickness_um, 1),
            'neg_coating_thickness_actual_um': round(r.neg_coating_thickness_actual_um, 1),
            'neg_coating_true_density_g_cm3': round(r.neg_coating_true_density_g_cm3, 4),
            'neg_coating_pressed_density_g_cm3': round(r.neg_coating_pressed_density_g_cm3, 2),
            'neg_coating_porosity': round(r.neg_coating_porosity * 100, 1),
            'neg_areal_capacity_mAh_cm2': round(r.neg_areal_capacity_mAh_cm2, 4),
            'neg_coating_area_cm2': round(r.neg_coating_area_cm2, 1),
            'neg_active_weight_g': round(r.neg_active_weight_g, 2),
            'neg_coating_weight_g': round(r.neg_coating_weight_g, 2),
            'neg_foil_weight_g': round(r.neg_foil_weight_g, 2),
            'neg_total_weight_g': round(r.neg_total_weight_g, 2),
            'neg_coating_volume_cm3': round(r.neg_coating_volume_cm3, 4),
            'neg_pore_volume_cm3': round(r.neg_pore_volume_cm3, 4),
            'neg_capacity_mAh': round(r.neg_capacity_mAh, 1),
            'actual_np_ratio': round(r.actual_np_ratio, 4),
            'areal_np_ratio': round(r.areal_np_ratio, 4),
            'separator_width_mm': round(r.separator_width_mm, 0),
            'separator_total_length_mm': round(r.separator_total_length_mm, 0),
            'separator_volume_cm3': round(r.separator_volume_cm3, 4),
            'separator_pore_volume_cm3': round(r.separator_pore_volume_cm3, 4),
            'separator_weight_g': round(r.separator_weight_g, 2),
            'unit_thickness_um': round(r.unit_thickness_um, 1),
            'total_winding_layers': r.total_winding_layers,
            'total_spiral_length_mm': round(r.total_spiral_length_mm, 0),
            'core_diameter_mm': round(r.core_diameter_mm, 2),
            'core_diameter_soc100_mm': round(r.core_diameter_soc100_mm, 2),
            'diameter_margin_mm': round(r.diameter_margin_mm, 3),
            'total_pore_volume_cm3': round(r.total_pore_volume_cm3, 4),
            'electrolyte_volume_cm3': round(r.electrolyte_volume_cm3, 2),
            'electrolyte_weight_g': round(r.electrolyte_weight_g, 2),
            'case_weight_g': round(r.case_weight_g, 2),
            'insulator_pos_weight_g': round(r.insulator_pos_weight_g, 3),
            'insulator_neg_weight_g': round(r.insulator_neg_weight_g, 3),
            'tab_pos_weight_g': round(r.tab_pos_weight_g, 3),
            'tab_neg_weight_g': round(r.tab_neg_weight_g, 3),
            'cap_weight_g': round(r.cap_weight_g, 3),
            'core_weight_g': round(r.core_weight_g, 2),
            'total_cell_weight_g': round(r.total_cell_weight_g, 2),
            'cell_volume_cm3': round(r.cell_volume_cm3, 2),
            'cell_energy_Wh': round(r.cell_energy_Wh, 2),
            'gravimetric_energy_Wh_kg': round(r.gravimetric_energy_Wh_kg, 0),
            'volumetric_energy_Wh_L': round(r.volumetric_energy_Wh_L, 0),
            'is_core_fit': r.is_core_fit,
            'is_np_safe': r.is_np_safe,
            'warnings': r.warnings,
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5555))
    app.run(host='0.0.0.0', port=port, debug=False)
