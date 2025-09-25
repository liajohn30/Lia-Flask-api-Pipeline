pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo 'Building Docker image...'
                sh 'docker build -t lia-flask-api .'
            }
        }

        stage('Test') {
            steps {
                echo 'Running unit tests...'
                sh 'docker run --rm lia-flask-api pytest'
            }
        }

        stage('Code Quality') {
            steps {
                echo 'Running flake8 lint checks...'
                sh 'docker run --rm lia-flask-api flake8 app.py'
            }
        }

        stage('Security Scan') {
            steps {
                echo 'Running Bandit security scan...'
        sh 'docker run --rm lia-flask-api bandit -r . || true'            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying container...'
                sh '''
          docker run -d --name lia-flask-api -p 5000:5000 lia-flask-api || true
        '''
            }
        }
    }

    post {
        always {
            echo 'Cleaning up...'
            sh 'docker stop lia-flask-api || true'
        }
    }
}
