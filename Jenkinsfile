pipeline {
agent any
stages {
    stage('Checkout') { steps { checkout scm } }
    stage('Install')  { steps { sh 'pip install -r requirements.txt' } }
    stage('Test')     { steps { sh 'pytest -q' } }
    stage('Deploy')   {
      when { expression { currentBuild.result == null || currentBuild.result == 'SUCCESS' } }
      steps {
        sh 'docker build -t ai_system:latest .'
        sh 'docker stop ai_system || true'
        sh 'docker rm ai_system || true'
        sh 'docker run -d --name ai_system -p 5000:5000 ai_system:latest'
      }
    }
  }
}
