# ScaleReport — Redesigned

Clean light-theme PyQt5 app with sidebar navigation.

## Structure

```
scale_app/
├── main.py                    # Entry point, font + auth setup
├── ui/
│   ├── style.qss              # All styling (light theme)
│   ├── components.py          # Reusable widget helpers
│   ├── sidebar.py             # Left nav sidebar
│   ├── app_window.py          # Main QMainWindow
│   └── pages/
│       ├── create_report.py   # ➕ New Report
│       ├── all_reports.py     # 📋 All Reports
│       ├── edit_report.py     # ✏️  Edit by ID
│       ├── search_report.py   # 🔍 Search by ID
│       └── by_client.py       # 👤 By Client
```

## Running

```bash
pip install PyQt5
cd scale_app
python main.py
```

## Connecting your real core/ backend

Every page has stub functions and clearly marked `# Real ... (uncomment)` blocks.
To wire up:

1. **Create page** — uncomment the `WeightData`, `addNewWeight`, `gen_report` block in `_submit()`
2. **All Reports** — replace `_stub_rows()` call in `load_data()` with `ARSTable(...).getDatasWithLimit()`
3. **Edit page** — uncomment `getWeightById` in `_load_record()` and `updateWeight` in `_save()`
4. **Search page** — uncomment `getWeightById` + `gen_report` in `_search()`
5. **By Client** — replace `_stub_rows_for()` with `ARSTable(...).getDatasWithKey(...)`
6. **Auth** — uncomment the `UserAuthApp` block in `main.py`

## Theming

All colors live in `ui/style.qss`. Key variables:
- Accent blue: `#2563EB`
- Surface: `#F5F6F8`
- Card bg: `#FFFFFF`
- Border: `#E2E5EA`
- Text primary: `#111827`
- Text secondary: `#6B7280`
