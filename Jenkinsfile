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
                sh 'docker run --rm lia-flask-api bandit -r . || true'
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying container...'
                sh '''
                  docker rm -f lia-flask-api || true
                  docker run -d --name lia-flask-api -p 5000:5000 lia-flask-api
                '''
            }
        }

        stage('Release') {
            environment {
                IMAGE = 'liajohn/lia-flask-api'
                TAG = "${env.BUILD_NUMBER}"
            }
            steps {
                echo 'Releasing Docker image to DockerHub...'
                withCredentials([usernamePassword(credentialsId: 'dockerhub', usernameVariable: 'DH_USER', passwordVariable: 'DH_PASS')]) {
                    sh '''
                      docker tag lia-flask-api ${IMAGE}:${TAG}
                      docker tag lia-flask-api ${IMAGE}:latest
                      echo "$DH_PASS" | docker login -u "$DH_USER" --password-stdin
                      docker push ${IMAGE}:${TAG}
                      docker push ${IMAGE}:latest
                    '''
                }
            }
        }

        stage('Monitoring') {
            steps {
                echo 'Checking application health...'
                sh '''
                  sleep 10
                  STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5000/)
                  if [ "$STATUS" -eq 200 ]; then
                    echo "App is healthy (HTTP 200)"
                  else
                    echo "Health check failed with status $STATUS"
                    exit 1
                  fi
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
