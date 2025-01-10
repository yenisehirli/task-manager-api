pipeline {
    agent {
        kubernetes {
            inheritFrom 'jenkins-agent'
            yaml '''
                apiVersion: v1
                kind: Pod
                spec:
                  containers:
                  - name: docker
                    image: docker:dind
                    securityContext:
                      privileged: true
                    env:
                    - name: DOCKER_HOST
                      value: unix:///var/run/docker.sock
                    volumeMounts:
                    - mountPath: /var/run/docker.sock
                      name: docker-sock
                  - name: sonar-scanner
                    image: sonarsource/sonar-scanner-cli:latest
                    command:
                    - cat
                    tty: true
                  volumes:
                  - name: docker-sock
                    hostPath:
                      path: /var/run/docker.sock
            '''
        }
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('SonarQube Analysis') {
            steps {
                container('sonar-scanner') {
                    withSonarQubeEnv('SonarQube') {
                        sh '''
                            sonar-scanner \
                            -Dsonar.host.url=http://10.43.16.30:30900 \
                            -Dsonar.token=$SONAR_TOKEN \
                            -Dsonar.projectKey=task-manager-api \
                            -Dsonar.projectName="Task Manager API" \
                            -Dsonar.sources=. \
                            -Dsonar.python.version=3.9
                        '''
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                container('docker') {
                    sh """
                        docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} .
                    """
                }
            }
        }

        stage('Push Docker Image') {
            environment {
                DOCKER_CREDENTIALS = credentials('docker-credentials')
            }
            steps {
                container('docker') {
                    sh '''
                        echo $DOCKER_CREDENTIALS_PSW | docker login -u $DOCKER_CREDENTIALS_USR --password-stdin
                        docker push ${DOCKER_IMAGE}:${DOCKER_TAG}
                        docker push ${DOCKER_IMAGE}:latest
                    '''
                }
            }
        }
    }
}