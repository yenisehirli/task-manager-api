pipeline {
    agent {
        kubernetes {
            yaml '''
                apiVersion: v1
                kind: Pod
                metadata:
                  labels:
                    jenkins: slave
                spec:
                  serviceAccountName: jenkins
                  containers:
                  - name: jnlp
                    image: jenkins/inbound-agent:latest
                    
                  # Docker container'ı - image build ve push işlemleri için
                  - name: docker
                    image: docker:dind
                    securityContext:
                      privileged: true
                    volumeMounts:
                    - name: docker-socket
                      mountPath: /var/run/docker.sock
                    tty: true
                    
                  # Python container'ı - SonarQube analizi için
                  - name: python
                    image: python:3.9-slim
                    command:
                    - cat
                    tty: true
                    
                  volumes:
                  - name: docker-socket
                    hostPath:
                      path: /var/run/docker.sock
            '''
            defaultContainer 'docker'
        }
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
                container('python') {
                    script {
                        def scannerHome = tool 'SonarQubeScanner'
                        withSonarQubeEnv('SonarQube') {
                            sh """
                                ${scannerHome}/bin/sonar-scanner \
                                -Dsonar.projectKey=task-manager-api \
                                -Dsonar.sources=. \
                                -Dsonar.python.version=3.9 \
                                -Dsonar.python.coverage.reportPaths=coverage.xml \
                                -Dsonar.sourceEncoding=UTF-8 \
                                -Dsonar.language=python \
                                -Dsonar.exclusions=**/*test*.py,**/migrations/**,**/__pycache__/**
                            """
                        }
                    }
                }
            }
        }
        
        stage('Quality Gate') {
            steps {
                timeout(time: 30, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }
        
        stage('Build Docker Image') {
            steps {
                container('docker') {
                    script {
                        sh """
                            docker build \
                                --cache-from ${DOCKER_IMAGE}:latest \
                                -t ${DOCKER_IMAGE}:${DOCKER_TAG} \
                                -t ${DOCKER_IMAGE}:latest .
                        """
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
                            docker.image("${DOCKER_IMAGE}:latest").push()
                        }
                    }
                }
            }
        }
    }
    
    post {
        always {
            cleanWs()
        }
        success {
            echo 'Pipeline başarıyla tamamlandı!'
        }
        failure {
            echo 'Pipeline başarısız oldu! Lütfen logları kontrol edin.'
        }
    }
}