pipeline {
    agent any
    options {
        disableConcurrentBuilds()
    }
    environment {
        DOCKER = "\"C:\\Users\\HP\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin\\docker.exe\""
        IMAGE_NAME = "mycompany/payment-app"
    }
    stages {
        stage('Build Base Image') {
            steps {
                echo "Building Docker Image for payment service..."
                bat "${DOCKER} build -t ${IMAGE_NAME}:latest ."
            }
        }

        stage('Deploy Blue (v1.0.0 - Stable)') {
            steps {
                echo "Deploying Blue environment on internal port 8081..."
                bat "@${DOCKER} stop payment-blue 2>nul & verify >nul"
                bat "@${DOCKER} rm payment-blue 2>nul & verify >nul"
                bat "${DOCKER} run -d --name payment-blue -p 8081:8080 -e APP_COLOR=BLUE -e APP_VERSION=1.0.0 ${IMAGE_NAME}:latest"
            }
        }

        stage('Start Production Router (Port 9090)') {
            steps {
                echo "Starting production Nginx gateway routing live traffic to Blue..."
                bat "@${DOCKER} stop payment-router 2>nul & verify >nul"
                bat "@${DOCKER} rm payment-router 2>nul & verify >nul"
                bat "${DOCKER} run -d --name payment-router -p 9090:9090 -v \"%WORKSPACE%\\nginx.conf:/etc/nginx/nginx.conf\" nginx:alpine"
            }
        }

        stage('Deploy Green (v2.0.0 - Defective)') {
            steps {
                echo "Deploying Green environment on staging port 8082..."
                bat "@${DOCKER} stop payment-green 2>nul & verify >nul"
                bat "@${DOCKER} rm payment-green 2>nul & verify >nul"
                bat "${DOCKER} run -d --name payment-green -p 8082:8080 -e APP_COLOR=GREEN -e APP_VERSION=2.0.0 ${IMAGE_NAME}:latest"
            }
        }

        stage('Promote Green to Production') {
            steps {
                echo "Switching live traffic router to Green (port 8082)..."
                // Overwrite content directly without altering file inode
                bat "${DOCKER} exec payment-router sh -c \"sed 's/8081/8082/g' /etc/nginx/nginx.conf > /tmp/nginx.conf && cp /tmp/nginx.conf /etc/nginx/nginx.conf\""
                bat "${DOCKER} exec payment-router nginx -s reload"
            }
        }

        stage('Simulate Failed Rollback Incident') {
            steps {
                echo "=========================================================="
                echo "INCIDENT: Error detected on Green! Engineer attempts container rollback..."
                echo "=========================================================="
                bat "${DOCKER} restart payment-green"
                echo "Result: Rollback failed! The production router still forwards traffic to Green."
            }
        }

        stage('Execute True Rollback') {
            steps {
                echo "=========================================================="
                echo "FIX: Executing instant traffic router switch back to Blue..."
                echo "=========================================================="
                // Revert router configuration back to Blue (8081)
                bat "${DOCKER} exec payment-router sh -c \"sed 's/8082/8081/g' /etc/nginx/nginx.conf > /tmp/nginx.conf && cp /tmp/nginx.conf /etc/nginx/nginx.conf\""
                bat "${DOCKER} exec payment-router nginx -s reload"
            }
        }
    }
    post {
        success {
            echo "SUCCESS: Lab 4 Blue-Green incident and true rollback completed on port 9090."
        }
        failure {
            echo "FAILURE: Lab 4 pipeline encountered an error."
        }
    }
}