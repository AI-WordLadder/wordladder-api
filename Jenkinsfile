pipeline {
    agent any

    environment {
        APP_NAME = 'wordladder-api'
    }

    stages {
        stage('Restart image') {
            steps {
                sh "docker stop wordladder-api"
                sh "docker rm wordladder-api"
            }
        }

        stage('Create Image') {
            steps {
                sh "ls -la"
                sh "docker build -t api_image ."
            }
        }

        stage('Run Image') {
            steps {
                sh "docker run -d --name ${APP_NAME} -p 8000:8000 api_image"
            }
        }
    }
}