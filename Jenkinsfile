pipeline {
    agent any

    environment {
        DOCKER_CREDENTIALS_ID = credentials('DOCKER_CREDENTIALS_ID')
        PATH = "/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin"
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
                             docker buildx build -t ${DOCKER_IMAGE_NAME}:${BUILD_NUMBER} \
                            --build-arg SECRET_KEY=${SECRET_KEY} \
                            --build-arg DB_NAME=${DB_NAME} \
                            --build-arg DB_USER=${DB_USER} \
                            --build-arg DB_PASSWORD=${DB_PASSWORD} \
                            --build-arg DB_HOST=${DB_HOST} \
                            --build-arg DB_PORT=${DB_PORT} \
                            --build-arg DJANGO_ENV=${DJANGO_ENV} \
                            --build-arg ALLOWED_HOSTS=${ALLOWED_HOSTS} .
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