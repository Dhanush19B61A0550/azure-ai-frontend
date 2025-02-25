pipeline {
    agent any

    environment {
        RESOURCE_GROUP = credentials('RESOURCE_GROUP')
        WEB_APP_NAME = credentials('WEB_APP_NAME')
    }

    stages {
        stage('Install') {
            steps {
                bat 'npm install'
            }
        }
        stage('Build') {
            steps {
                bat 'npm run build'
            }
        }
        stage('Test') {
            steps {
                bat 'npm test'
            }
        }
        stage('Deploy') {
            steps {
                bat """
                az webapp deployment source config-zip ^
                --resource-group %RESOURCE_GROUP% ^
                --name %WEB_APP_NAME% ^
                --src build
                """
            }
        }
    }
}
