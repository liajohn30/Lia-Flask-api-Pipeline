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
                sh 'docker run --rm lia-flask-api bandit -r .'
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying container...'
                sh 'docker run -d -p 5000:5000 --name lia-flask-api lia-flask-api'
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
