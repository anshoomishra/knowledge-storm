pipeline {
    agent any

    environment {
        DOCKER_CREDENTIALS_ID = credentials('DOCKER_CREDENTIALS_ID')
        DOCKER_IMAGE_NAME = 'anshoo/deepwater'
        GIT_REPO_URL = 'https://github.com/anshoomishra/deepwater.git'
        SECRET_KEY = credentials('SECRET_KEY') // Using Jenkins Credentials Plugin
        DB_NAME = credentials('DB_NAME')
        DB_USER = credentials('DB_USER')
        DB_PASSWORD = credentials('DB_PASSWORD')
        DB_HOST = credentials('DB_HOST')
        DB_PORT = credentials('DB_PORT')
        ALLOWED_HOSTS = credentials('ALLOWED_HOSTS')
        DJANGO_ENV = credentials('DJANGO_ENV')
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', credentialsId: 'your-github-credentials-id', url: GIT_REPO_URL
            }
        }

        stage('Build Docker Image') {
            steps {

                    sh '''#!/bin/bash
                             docker build -t ${DOCKER_IMAGE_NAME}:${BUILD_NUMBER} .
                        '''
            }
        }

        stage('Login to DockerHub') {
            steps {
                script {
                    sh 'echo $DOCKER_CREDENTIALS_ID_PSW | docker login -u $DOCKER_CREDENTIALS_ID_USR --password-stdin'
                }
            }
        }

        stage('Push Image') {
            steps {
                script {
                    sh 'docker push $DOCKER_IMAGE_NAME:$BUILD_NUMBER'
                }
            }
        }
    }
}