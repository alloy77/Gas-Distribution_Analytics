pipeline {
  agent any

  stages {
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
  }

  post {
    success {
      archiveArtifacts artifacts: 'tests/reports/results.xml', fingerprint: true
      echo 'Pipeline success'
    }
    failure {
      echo 'Pipeline failure'
    }
  }
}