# -*- coding: utf-8 -*-
"""Клиент API генерации строк плана работ (fastApiZima /work_plan_rows/generate)."""

from __future__ import annotations

from typing import Any, List, Optional

from server_response import ApiClient
from work_plan_rows_context import data_well_to_context

# Операции, для которых запрос уходит на сервер (остальные — без HTTP).
REMOTE_OPERATIONS = frozenset(
    {
        "torpedo",
        "clay_solution",
        "drilling",
        "sand_filling",
        "gpp",
        "grp",
        "raiding",
        "vp_cm",
        "opressovka",
        "geophysic",
        "izv_paker",
        "emergency_lar",
        "block_pack_work",
        "perforation",
        "main_privyazka_nkt",
        "main_pressure_gis",
        "main_definition_bottom_gklm",
        "main_rgd_without_paker",
        "main_rgd_with_paker",
        "main_definition_q",
        "main_definition_q_nek",
        "main_kot_work",
        "main_konte_action",
        "main_mkp_revision",
        "main_resuscitation_work",
        "main_pvo_cat1",
        "main_washing_sand",
        "main_empty_string_row",
        "main_po_emergency_ecn",
        "main_hook",
        "main_lapel_tubing",
        "main_emergency_sticking",
        "opressovka_aspo",
        "emergency_printing",
        "main_frezering_port",
        "tubing_pressuar_testing",
        "acids",
        "emergency_magnit",
        "kompress",
        "change_fluid",
        "pero_work",
        "emergency_po",
        "descent_gno",
        "gno_lift",
        "sgm_work",
        "swabbing",
        "template_work",
        "template_without_skm",
        "rir",
        "acid_paker",
        "gnkt_after_grp",
        "gnkt_bopz",
        "gnkt_opz",
        "gnkt_frez",
    }
)


def _normalize_rows(rows: Any) -> Optional[List[List[Any]]]:
    if not isinstance(rows, list):
        return None
    out: List[List[Any]] = []
    for row in rows:
        if not isinstance(row, list):
            return None
        out.append([None if c is None else c for c in row])
    return out


def try_generate_work_rows(
    operation: str,
    data_well: Any,
    params: dict,
    work_plan: Optional[str] = None,
) -> Optional[List[List[Any]]]:
    """
    Возвращает work_list с сервера или None (нет сети, ошибка, операция не на сервере).
    """
    if params.get("_skip_remote"):
        return None
    if operation not in REMOTE_OPERATIONS:
        return None
    wp = work_plan if work_plan is not None else getattr(data_well, "work_plan", "krs")
    body = {
        "schema_version": 1,
        "work_plan": wp,
        "operation": operation,
        "well_context": data_well_to_context(data_well, wp),
        "params": params,
    }
    result = ApiClient.request_post_json_silent(
        ApiClient.work_plan_rows_generate_path(), body
    )
    if not result or "rows" not in result:
        return None
    return _normalize_rows(result["rows"])
