# Commands

### One-time setup
```bash
modal run models.py::download_models
```

### Run
```bash
modal run batch.py::batch --pairs-file ../pairs.md
```

### Get outputs
```bash
modal volume get bbq-outputs / .
```

### Clear outputs
```bash
modal volume delete bbq-outputs -y
```

### List outputs
```bash
modal volume ls bbq-outputs
```
