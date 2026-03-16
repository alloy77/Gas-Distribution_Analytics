pipeline {
  agent any

  environment {
    PYTHON = 'python'
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Install Dependencies') {
      steps {
        script {
          if (fileExists('requirements.txt')) {
            sh 'python -m pip install --upgrade pip'
            sh 'python -m pip install -r requirements.txt'
          } else {
            echo 'requirements.txt not found, skipping dependency install.'
          }
        }
      }
    }

    stage('Run Tests') {
      steps {
        sh 'pytest -q --junitxml=tests/reports/results.xml'
      }
    }

    stage('Run Pipelines') {
      steps {
        sh 'python -m pipelines.raw_data_watcher'
      }
    }
  }

  post {
    success {
      archiveArtifacts artifacts: 'tests/reports/results.xml', fingerprint: true
      echo 'Jenkins pipeline succeeded.'
    }
    failure {
      echo 'Jenkins pipeline failed.'
    }
  }
}
