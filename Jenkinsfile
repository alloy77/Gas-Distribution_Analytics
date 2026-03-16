stage('Install Dependencies') {
  steps {
    bat 'python -m pip install --upgrade pip'
    bat 'python -m pip install -r requirements.txt'
  }
}

stage('Run Tests') {
  steps {
    bat 'pytest -q --junitxml=tests/reports/results.xml'
  }
}

stage('Run Pipelines') {
  steps {
    bat 'python -m pipelines.raw_data_watcher'
  }
}