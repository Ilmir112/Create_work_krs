# -*- coding: utf-8 -*-
"""Сериализация data_well (FindIndexPZ) для API генерации строк плана работ."""

from __future__ import annotations

import json
from typing import Any, Mapping, Optional

import data_list


def _get_attr(obj: Any, name: str, default: Any = None) -> Any:
    if obj is None:
        return default
    if hasattr(obj, name):
        return getattr(obj, name, default)
    return default


def _unwrap_protected(value: Any) -> Any:
    if value is None:
        return None
    if hasattr(value, "get_value"):
        return value.get_value
    return value


def _json_safe(obj: Any) -> Any:
    if isinstance(obj, Mapping):
        return {str(k): _json_safe(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_json_safe(x) for x in obj]
    if isinstance(obj, (str, int, float, bool)) or obj is None:
        return obj
    try:
        json.dumps(obj)
        return obj
    except (TypeError, ValueError):
        return str(obj)


def _to_float(v: Any, default: float = 0.0) -> float:
    if v is None or v == "":
        return default
    try:
        return float(v)
    except (TypeError, ValueError):
        return default


def previous_current_bottom_for_kot(data_well: Any) -> float:
    """Забой до операции КОТ (для main_kot_work на API)."""
    return _to_float(_unwrap_protected(_get_attr(data_well, "current_bottom")))


def data_well_to_context(data_well: Any, work_plan: Optional[str] = None) -> dict[str, Any]:
    """
    Минимальный контекст для серверных билдеров.
    Расширяйте по мере переноса операций на API.
    """
    wp = work_plan if work_plan is not None else getattr(data_well, "work_plan", "krs")
    contractor_key = getattr(data_list, "contractor", "") or ""
    pvo_date = ""
    try:
        pvo_date = str(
            data_list.DICT_CONTRACTOR.get(contractor_key, {}).get("Дата ПВО", "") or ""
        )
    except (TypeError, AttributeError, KeyError):
        pvo_date = ""
    ctx: dict[str, Any] = {
        "schema_version": 1,
        "work_plan": wp,
        "contractor": contractor_key,
        "region": str(_unwrap_protected(_get_attr(data_well, "region")) or ""),
        "expected_pressure": _to_float(_get_attr(data_well, "expected_pressure")),
        "pvo_scheme_date": pvo_date,
        "column_additional": bool(_unwrap_protected(_get_attr(data_well, "column_additional"))),
        "column_diameter": _to_float(_unwrap_protected(_get_attr(data_well, "column_diameter"))),
        "column_wall_thickness": _to_float(
            _unwrap_protected(_get_attr(data_well, "column_wall_thickness"))
        ),
        "head_column": _to_float(_unwrap_protected(_get_attr(data_well, "head_column"))),
        "diameter_doloto_ek": _to_float(_unwrap_protected(_get_attr(data_well, "diameter_doloto_ek"))),
        "column_additional_diameter": _to_float(
            _unwrap_protected(_get_attr(data_well, "column_additional_diameter"))
        ),
        "column_additional_wall_thickness": _to_float(
            _unwrap_protected(_get_attr(data_well, "column_additional_wall_thickness"))
        ),
        "head_column_additional": _to_float(
            _unwrap_protected(_get_attr(data_well, "head_column_additional"))
        ),
        "current_bottom": _to_float(_unwrap_protected(_get_attr(data_well, "current_bottom"))),
        "static_level": _to_float(_unwrap_protected(_get_attr(data_well, "static_level"))),
        "max_admissible_pressure": _to_float(
            _unwrap_protected(_get_attr(data_well, "max_admissible_pressure"))
        ),
        "max_expected_pressure": _to_float(
            _unwrap_protected(_get_attr(data_well, "max_expected_pressure"))
        ),
        "curator": str(_unwrap_protected(_get_attr(data_well, "curator")) or ""),
        "fluid_work": str(_unwrap_protected(_get_attr(data_well, "fluid_work")) or ""),
        "nkt_template": _unwrap_protected(_get_attr(data_well, "nkt_template")),
        "nkt_diam": _unwrap_protected(_get_attr(data_well, "nkt_diam")),
        "perforation_roof": _to_float(_unwrap_protected(_get_attr(data_well, "perforation_roof"))),
        "dict_nkt_before": _json_safe(_get_attr(data_well, "dict_nkt_before") or {}),
        "dict_sucker_rod": _json_safe(_get_attr(data_well, "dict_sucker_rod") or {}),
        "depth_fond_paker_before": _to_float(
            _unwrap_protected((_get_attr(data_well, "depth_fond_paker_before") or {}).get("before"))
        ),
        "dict_perforation": _json_safe(_get_attr(data_well, "dict_perforation") or {}),
        "plast_work": _json_safe(_get_attr(data_well, "plast_work") or []),
        "bottom_hole_artificial": _to_float(
            _unwrap_protected(_get_attr(data_well, "bottom_hole_artificial"))
        ),
        "dict_pump_ecn": _json_safe(_get_attr(data_well, "dict_pump_ecn") or {}),
        "dict_pump_shgn": _json_safe(_get_attr(data_well, "dict_pump_shgn") or {}),
        "paker_before_before": str(
            _unwrap_protected((_get_attr(data_well, "paker_before") or {}).get("before")) or ""
        ),
        # Для проверки опрессовки/глубинных условий (например, drilling.check_pressure()).
        "leakiness": bool(_unwrap_protected(_get_attr(data_well, "leakiness"))),
        "dict_leakiness": _json_safe(_get_attr(data_well, "dict_leakiness") or {}),
        # need_h2s / смена ЖГС (свабирование и др.)
        "dict_category": _json_safe(_get_attr(data_well, "dict_category") or {}),
        "plast_project": _json_safe(_get_attr(data_well, "plast_project") or []),
        # Инклинометрия (gpp и др.)
        "max_angle": _to_float(_unwrap_protected(_get_attr(data_well, "max_angle"))),
        "max_angle_depth": _to_float(_unwrap_protected(_get_attr(data_well, "max_angle_depth"))),
        "angle_data": _json_safe(_get_attr(data_well, "angle_data") or []),
        # grp / pvo_gno / testing_pressure (plast_all как в Qt parent_work.testing_pressure)
        "plast_all": _json_safe(_get_attr(data_well, "plast_all") or []),
        "category_pvo": _unwrap_protected(_get_attr(data_well, "category_pvo")),
        "category_h2s": str(_unwrap_protected(_get_attr(data_well, "category_h2s")) or ""),
        "category_gas_factor": str(_unwrap_protected(_get_attr(data_well, "category_gas_factor")) or ""),
        # descent_gno
        "dict_nkt_after": _json_safe(_get_attr(data_well, "dict_nkt_after") or {}),
        "dict_sucker_rod_after": _json_safe(_get_attr(data_well, "dict_sucker_rod_after") or {}),
        "paker_after": str(
            _unwrap_protected((_get_attr(data_well, "paker_before") or {}).get("after")) or ""
        ),
        "depth_fond_paker_after": _to_float(
            _unwrap_protected((_get_attr(data_well, "depth_fond_paker_before") or {}).get("after"))
        ),
        "depth_fond_paker_second_after": _to_float(
            _unwrap_protected((_get_attr(data_well, "depth_fond_paker_second_before") or {}).get("after"))
        ),
        "dict_pump_ecn_depth_after": _to_float(
            _unwrap_protected((_get_attr(data_well, "dict_pump_ecn_depth") or {}).get("after"))
        ),
        "dict_pump_shgn_depth_after": _to_float(
            _unwrap_protected((_get_attr(data_well, "dict_pump_shgn_depth") or {}).get("after"))
        ),
        "template_depth": _to_float(_unwrap_protected(_get_attr(data_well, "template_depth"))),
        "template_depth_addition": _to_float(
            _unwrap_protected(_get_attr(data_well, "template_depth_addition"))
        ),
        "skm_depth": _to_float(_unwrap_protected(_get_attr(data_well, "skm_depth"))),
        "well_number": str(_unwrap_protected(_get_attr(data_well, "well_number")) or ""),
        "well_area": str(_unwrap_protected(_get_attr(data_well, "well_area")) or ""),
        "fluid_work_short": (
            str(_unwrap_protected(_get_attr(data_well, "fluid_work_short")))
            if _unwrap_protected(_get_attr(data_well, "fluid_work_short")) not in (None, "")
            else (str(_unwrap_protected(_get_attr(data_well, "fluid_work")) or "")[:4])
        ),
        "gips_in_well": bool(_unwrap_protected(_get_attr(data_well, "gips_in_well"))),
        "type_kr": str(_unwrap_protected(_get_attr(data_well, "type_kr")) or ""),
        "bvo": bool(_unwrap_protected(_get_attr(data_well, "bvo"))),
        "dict_pump_ecn_depth_before": _to_float(
            _unwrap_protected((_get_attr(data_well, "dict_pump_ecn_depth") or {}).get("before"))
        ),
        "dict_pump_shgn_depth_before": _to_float(
            _unwrap_protected((_get_attr(data_well, "dict_pump_shgn_depth") or {}).get("before"))
        ),
        # РИР (rir_plan_engine): башмаки, кондуктор
        "shoe_column": _to_float(_unwrap_protected(_get_attr(data_well, "shoe_column"))),
        "shoe_column_additional": _to_float(
            _unwrap_protected(_get_attr(data_well, "shoe_column_additional"))
        ),
        "column_conductor_length": _to_float(
            _unwrap_protected(_get_attr(data_well, "column_conductor_length"))
        ),
    }
    return ctx
