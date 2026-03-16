import hashlib
import json
import os
from pathlib import Path

watch_file = Path('data/raw/CGD_Raw.csv')
state_file = Path('.pipeline_state.json')


def file_hash(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()


def load_state() -> dict:
    if state_file.exists():
        return json.loads(state_file.read_text())
    return {}


def save_state(state: dict):
    state_file.write_text(json.dumps(state, indent=2))


def run_pipelines():
    print('Detected new raw data or first run. Running pipelines...')
    os.system('python -m pipelines.cleaning_pipeline')
    os.system('python -m pipelines.transformation_pipeline')
    os.system('python -m pipelines.analytics_pipeline')
    os.system('python -m pipelines.ml_pipeline')


def main():
    if not watch_file.exists():
        raise FileNotFoundError(f'Raw dataset not found: {watch_file}')

    current = file_hash(watch_file)
    state = load_state()
    last = state.get('raw_data_hash')

    if last == current:
        print('Raw dataset has not changed since last run. Skipping pipeline execution.')
        return 0

    run_pipelines()
    state['raw_data_hash'] = current
    save_state(state)
    print('Pipeline completed and state updated.')
    return 0


if __name__ == '__main__':
    exit(main())
