# Sentinel

A modular Python desktop application.

## Run

```bash
cd sentinel
python main.py
```

Expected output:
```
Sentinel online  (v0.1.0)
```

## Project layout

```
sentinel/
├── main.py               # Entry point — run this
├── sentinel/
│   ├── config.py         # Global constants (name, version, …)
│   ├── core/
│   │   └── system.py     # Startup / shutdown controller
│   └── modules/
│       └── __init__.py   # BaseModule + ModuleRegistry
└── README.md
```

## Adding a new feature

1. Create `sentinel/modules/<feature>.py`.
2. Define a class that inherits from `BaseModule` and implements `run()`.
3. Register it in `sentinel/core/system.py` → `_load_modules()`.

That's it — the registry picks it up automatically on the next run.
