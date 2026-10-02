pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo 'Код получен из GitHub'
            }
        }

        stage('Install dependencies') {
            steps {
                bat 'pip install -r requirements.txt'
            }
        }

        stage('Run tests') {
            steps {
                bat 'pytest tests/ --junitxml=reports/results.xml'
            }
        }

        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                echo 'Развертывание приложения...'
            }
        }
    }

    post {
        always {
            junit 'reports/results.xml'
        }
    }
}