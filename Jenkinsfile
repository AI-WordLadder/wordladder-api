pipeline {
    agent any

    stages {
        stage('Create Image') {
            steps {
                sh "ls -la"
                sh "docker build -t api_image ."
            }
        }

        stage('Run Image') {
            steps {
                sh "docker run -d --name wordladder-api -p 8000:8000 api_image"
            }
        }
    }
}