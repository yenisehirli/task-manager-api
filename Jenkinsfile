pipeline {
    agent {
        kubernetes {
            inheritFrom 'jenkins-agent'
            defaultContainer 'docker'
        }
    }
    triggers {
        githubPush()
    }
    
    environment {
        DOCKER_IMAGE = 'yenisehirli/task-manager-api'
        DOCKER_TAG = "${BUILD_NUMBER}"
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('SonarQube Analysis') {
    steps {
        withSonarQubeEnv('SonarQube') {
            sh """
                ${tool('SonarQubeScanner')}/bin/sonar-scanner \
                -Dsonar.projectKey=task-manager-api \
                -Dsonar.projectName='Task Manager API' \
                -Dsonar.sources=. \
                -Dsonar.python.version=3.9 \
                -Dsonar.qualitygate.wait=true
            """
        }
    }
}

stage('Quality Gate') {
    steps {
        timeout(time: 2, unit: 'MINUTES') {
            waitForQualityGate abortPipeline: true
        }
    }
}
        
        stage('Build Docker Image') {
            steps {
                container('docker') {
                    script {
                        docker.build("${DOCKER_IMAGE}:${DOCKER_TAG}")
                    }
                }
            }
        }
        
        stage('Push Docker Image') {
            steps {
                container('docker') {
                    script {
                        docker.withRegistry('https://registry.hub.docker.com', 'docker-credentials') {
                            docker.image("${DOCKER_IMAGE}:${DOCKER_TAG}").push()
                            docker.image("${DOCKER_IMAGE}:${DOCKER_TAG}").push('latest')
                        }
                    }
                }
            }
        }
    }
}