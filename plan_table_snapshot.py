"""Сериализация / восстановление QTableWidget для Redis-кэша плана работ."""

from __future__ import annotations

import json
from typing import Any, Dict, List

from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem

SNAPSHOT_VERSION = 1


def table_snapshot_to_dict(table: QTableWidget, data_well: Any) -> Dict[str, Any]:
    rows = table.rowCount()
    cols = table.columnCount()
    cells: List[List[str]] = []
    for r in range(rows):
        row: List[str] = []
        for c in range(cols):
            it = table.item(r, c)
            row.append(it.text() if it is not None else "")
        cells.append(row)

    spans: List[List[int]] = []
    seen = set()
    for r in range(rows):
        for c in range(cols):
            rs = table.rowSpan(r, c)
            cs = table.columnSpan(r, c)
            if rs > 1 or cs > 1:
                key = (r, c, rs, cs)
                if key not in seen:
                    seen.add(key)
                    spans.append([r, c, rs, cs])

    heights: List[float] = []
    for r in range(rows):
        heights.append(float(table.rowHeight(r)))

    insert_index2 = getattr(data_well, "insert_index2", None)

    data_list_raw = getattr(data_well, "data_list", [])
    try:
        data_list_json = json.dumps(data_list_raw, ensure_ascii=False, default=str)
    except Exception:
        data_list_json = "[]"

    return {
        "version": SNAPSHOT_VERSION,
        "rows": rows,
        "cols": cols,
        "cells": cells,
        "spans": spans,
        "row_heights": heights,
        "insert_index2": insert_index2,
        "data_list_json": data_list_json,
    }


def apply_table_snapshot(
    table: QTableWidget, data_well: Any, payload: Dict[str, Any]
) -> None:
    ver = payload.get("version", 0)
    if ver != SNAPSHOT_VERSION:
        print(f"plan_table_snapshot: неизвестная версия снимка {ver}")

    rows = int(payload.get("rows", 0))
    cols = int(payload.get("cols", 0))
    cells = payload.get("cells") or []

    model = table.model()
    table.blockSignals(True)
    model.blockSignals(True)
    try:
        table.clearContents()
        table.setRowCount(rows)
        table.setColumnCount(cols)

        for r in range(min(rows, len(cells))):
            row = cells[r]
            for c in range(min(cols, len(row))):
                table.setItem(r, c, QTableWidgetItem(str(row[c])))

        for span in payload.get("spans") or []:
            if len(span) >= 4:
                r, c, rs, cs = (
                    int(span[0]),
                    int(span[1]),
                    int(span[2]),
                    int(span[3]),
                )
                if rs > 1 or cs > 1:
                    table.setSpan(r, c, rs, cs)

        for r, h in enumerate(payload.get("row_heights") or []):
            try:
                table.setRowHeight(r, int(h))
            except Exception:
                pass

        ins = payload.get("insert_index2")
        if ins is not None:
            try:
                data_well.insert_index2 = int(ins)
            except Exception:
                data_well.insert_index2 = ins

        dl = payload.get("data_list_json")
        if dl:
            try:
                data_well.data_list = json.loads(dl)
            except Exception:
                pass

        try:
            data_well.count_row_well = table.rowCount()
        except Exception:
            pass
    finally:
        model.blockSignals(False)
        table.blockSignals(False)
