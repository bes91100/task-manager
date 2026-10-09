pipeline {
    agent any

    environment {
        BRANCH = "${env.BRANCH_NAME ?: env.GIT_BRANCH?.replace('origin/', '') ?: 'main'}"
    }

    stages {
        stage('Checkout') {
            steps {
                echo "=== Текущая ветка: ${env.BRANCH} ==="
                echo 'Код успешно получен из GitHub'
            }
        }

        stage('Install dependencies') {
            steps {
                echo '=== Установка зависимостей ==='
                bat 'pip install -r requirements.txt'
            }
        }

        stage('Run tests') {
            steps {
                echo '=== Запуск автотестов ==='
                bat 'pytest tests/ --junitxml=reports/results.xml -v'
            }
        }

        stage('Deploy (CD)') {
            when {
                expression { env.BRANCH == 'main' }
            }
            steps {
                echo '=== Развертывание приложения (CD) ==='
                echo "Развертывание ветки ${env.BRANCH}..."
                echo 'Артефакт: reports/results.xml'
                echo 'Развертывание завершено успешно'
            }
        }
    }

    post {
        always {
            echo '=== Публикация отчёта о тестах ==='
            junit 'reports/results.xml'
        }
        success {
            echo 'Пайплайн успешно завершён'
        }
        failure {
            echo 'Пайплайн завершился с ошибкой'
        }
    }
}