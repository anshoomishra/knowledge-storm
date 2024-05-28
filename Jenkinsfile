pipeline {
    agent any

    environment {
        DOCKER_CREDENTIALS_ID = credentials('dockerhubid')
        DOCKER_IMAGE_NAME = 'anshoo/simple_crud'
        GIT_REPO_URL = 'https://github.com/anshoomishra/simple_crud.git'
        SECRET_KEY = credentials('SECRET_KEY') // Using Jenkins Credentials Plugin
        DB_NAME = credentials('DB_NAME')
        DB_USER = credentials('DB_USER')
        DB_PASSWORD = credentials('DB_PASSWORD')
        DB_HOST = credentials('DB_HOST')
        DB_PORT = '5432'
        ALLOWED_HOSTS = 'yourdomain.com,www.yourdomain.com'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', credentialsId: 'your-github-credentials-id', url: GIT_REPO_URL
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${DOCKER_IMAGE_NAME}:${BUILD_NUMBER}",
                    "--build-arg SECRET_KEY=${env.SECRET_KEY} \
                         --build-arg DB_NAME=${env.DB_NAME} \
                         --build-arg DB_USER=${env.DB_USER} \
                         --build-arg DB_PASSWORD=${env.DB_PASSWORD} \
                         --build-arg DB_HOST=${env.DB_HOST} \
                         --build-arg DB_PORT=${env.DB_PORT} \
                         --build-arg ALLOWED_HOSTS=${env.ALLOWED_HOSTS} ."
                    )
                }
            }
        }

        stage('login to dockerhub') {
            steps{
                sh 'echo $DOCKER_CREDENTIALS_ID_PSW | docker login -u $DOCKER_CREDENTIALS_ID_USR --password-stdin'
            }
        }
        stage('push image') {
            steps{
                sh 'docker push $DOCKER_IMAGE_NAME:$BUILD_NUMBER'
            }
        }
    }
}