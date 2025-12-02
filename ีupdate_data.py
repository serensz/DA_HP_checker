import pandas as pd
import json
from pathlib import Path
import re

ROOT = Path(__file__).parent
CSV_FILE = ROOT / "data" / "boss_hp_master.csv"
JSON_OUT = ROOT / "public" / "bosses.json"

LINK_COL = "link"  # หรือ "boss_link" ถ้าพี่เปลี่ยนชื่อไว้

def main():
    if not CSV_FILE.exists():
        raise SystemExit(f"ไม่พบไฟล์ {CSV_FILE}")

    df = pd.read_csv(CSV_FILE)

    required = [LINK_COL, "Date", "boss_name", "boss_hp"]
    for col in required:
        if col not in df.columns:
            raise SystemExit(f"CSV ไม่มีคอลัมน์ '{col}' (พบ {list(df.columns)})")

    # แปลงข้อมูลให้สะอาด
    df["boss_hp"] = pd.to_numeric(df["boss_hp"], errors="coerce")
    df["boss_id"] = df[LINK_COL].str.extract(r"(\d+)$").astype(int)
    df["date_start"] = pd.to_datetime(df["Date"], errors="coerce")

    df = df.dropna(subset=["date_start", "boss_hp", "boss_name"])

    # กันข้อมูลซ้ำ
    df = (
        df.sort_values(["boss_id", "date_start"])
          .drop_duplicates(subset=["boss_id", "date_start", "boss_name"], keep="last")
          .reset_index(drop=True)
    )

    # สร้าง JSON ให้ Svelte ใช้
    result = []
    for name, grp in df.groupby("boss_name"):
        grp = grp.sort_values("date_start")
        timeline = []
        for _, row in grp.iterrows():
            timeline.append({
                "date": row["date_start"].strftime("%Y-%m-%d"),
                "hp": int(row["boss_hp"]),
                "boss_id": int(row["boss_id"]),
            })
        result.append({
            "boss_name": name,
            "timeline": timeline
        })

    JSON_OUT.parent.mkdir(parents=True, exist_ok=True)
    JSON_OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    print("✔ bosses.json สร้างเสร็จแล้ว")
    print("✔ จำนวนบอสทั้งหมด:", len(result))


if __name__ == "__main__":
    main()
