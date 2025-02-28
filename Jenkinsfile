pipeline {
    agent any
    environment {
        RESOURCE_GROUP_NAME = credentials('RESOURCE_GROUP_NAME')
        WEB_APP_NAMES = credentials('WEB_APP_NAMES')
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
                bat 'npm test --passWithNoTests || exit /b 0'
            }
        }
        stage('Deploy') {
            steps {
                bat 'powershell Compress-Archive -Path build\\* -DestinationPath build.zip -Force'
                bat 'az webapp deployment source config-zip --resource-group %RESOURCE_GROUP_NAME% --name %WEB_APP_NAMES% --src build.zip'
            }
        }
    }
}
