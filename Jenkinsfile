pipeline {
    agent any

    environment {
        NETLIFY_SITE_ID = '8599b32b-e88a-41e1-8586-6c366a135701'
        NETLIFY_AUTH_TOKEN = credentials('netlify-token')
        APP_NAME = 'wordladder-api'
    }

    stages {
        stage('Create Image') {
            steps {
                sh "docker build -t api_image ."
            }
        }

        stage('Run Image') {
            steps {
                sh "docker run -d --name ${APP_NAME} -p 8000:8000 api_image"
            }
        }

        // stage('Deploy') {
        //     steps {
        //         sh ""
        //     }
        // }
    }
}