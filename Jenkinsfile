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
                  docker run -d --name lia-flask-api -p 5000:5000 lia-flask-api || true
                '''
            }
        }

        stage('Release') {
            environment {
                IMAGE = 'liajohn30/lia-flask-api'
                TAG = "${env.BUILD_NUMBER}"
            }
            steps {
                echo 'Releasing Docker image to DockerHub...'
                withCredentials([usernamePassword(credentialsId: 'dockerhub', usernameVariable: 'DH_USER', passwordVariable: 'DH_PASS')]) {
                    sh """
                        docker tag lia-flask-api ${IMAGE}:${TAG}
                        docker tag lia-flask-api ${IMAGE}:latest
                        echo "$DH_PASS" | docker login -u "$DH_USER" --password-stdin
                        docker push ${IMAGE}:${TAG}
                        docker push ${IMAGE}:latest
                    """
                }
            }
        }

        stage('Monitoring') {
            steps {
                echo 'Checking application health...'
                // Wait a bit for container startup
                sh 'sleep 5'
                // Use curl to hit health endpoint
                sh '''
                  if curl -s http://localhost:5000/ | grep "Welcome Lia"; then
                    echo "Health check passed!"
                  else
                    echo "Health check failed!"
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
