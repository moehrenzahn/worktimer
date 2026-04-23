# WorkTimer

A Python CLI tool for tracking work sessions, breaks, overtime, and generating reports. Stores data as YAML in `database/work.yaml`.

## Running

```bash
python3 WorkTimer.py [command] [options]
```

Key commands:
- (no args) — display current timer status
- `timer [category] [summary]` — start/stop work timer
- `pause` — start/stop break
- `update [category] [summary]` — change current session's category/summary
- `export` — export to text file
- `report` — generate Excel/ODS report
- `sync` — sync with remote git repo
- `log` — open log in editor
- `import [file]` — import a work log

## Testing

```bash
python3 -m unittest   # run all tests
make test             # same via Makefile
```

Test dependencies: `pip3 install freezegun`

Tests live in `test/` (unit) and `test/integration/` (integration). Time is mocked with `freezegun`.

## Architecture

```
WorkTimer.py        entry point
main.py             CLI argument parsing and command dispatch
config.py           config loader (merges config_default.json + config.json + CLI flags)

actions/            one file per command (timer, pause, change, export, report, sync, log, add, holidays)
data/               domain models
  day.py            single work day (goal hours, work blocks, overtime calculation)
  days.py           collection of Day objects with aggregate stats
  block/work.py     work interval (start, stop, category, summary)
  block/pause.py    break interval
storage/            YAML and JSON persistence
output/             display (terminal status, macOS notifications, iMessage, xBar elements)
exporter/           report generators (text, Excel, ODS)
importer/           import support (modern + legacy format)
```

## Data Format

Work log is YAML (`database/work.yaml`):

```yaml
'2021-08-02':
  date: '2021-08-02'
  goal: '8:00'
  work:
  - category: div
    start: '8:22'
    stop: '12:15'
  - category: project
    start: '12:55'
    stop: '17:56'
    summary: 'Feature implementation'
```

## Configuration

`config_default.json` holds all defaults. `config.json` holds user overrides. Key settings:

| Key | Default | Description |
|-----|---------|-------------|
| `hours_per_day` | 8 | Daily work goal |
| `categories` | `{}` | Named categories |
| `notifications` | true | macOS notifications |
| `textbar` | false | xBar plugin mode |
| `sync_repo_url` | `""` | Git repo for syncing |
| `holiday_bundesland` | null | German state for holidays |
| `overtime_offset_in_minutes` | 0 | Initial overtime carry-over |

## Platform Notes

- macOS only (uses Notification Center and optionally Messages.app)
- xBar plugin integration for menu bar display
- German public holiday support (`berechnung_feiertage.py`)
