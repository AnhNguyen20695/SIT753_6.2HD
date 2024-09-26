pipeline {
    agent any

    environment {
        AWS_DEFAULT_REGION = 'ap-southeast-2'
        AWS_ACCOUNT_ID = '277707121057'
        ECR_REPOSITORY = 'https://277707121057.dkr.ecr.ap-southeast-2.amazonaws.com/sit753'
        IMAGE_TAG = "latest" // Or use a dynamic tag based on build number or git commit
        EB_APPLICATION_NAME = 'sit753-s222521972-test-server'
        EB_ENVIRONMENT_NAME = 'sit753-s222521972-test-server-env'
        S3_BUCKET = 'elasticbeanstalk-ap-southeast-2-277707121057'
    }
    options {
        skipStagesAfterUnstable()
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/AnhNguyen20695/SIT753_6.2HD.git'
            }
        }

        stage ('Stop previous running container'){
            steps{
                sh returnStatus: true, script: 'docker stop $(docker ps -a | grep ${JOB_NAME} | awk \'{print $1}\')'
                sh returnStatus: true, script: 'docker rmi $(docker images | grep ${registry} | awk \'{print $3}\') --force' //this will delete all images
                sh returnStatus: true, script: 'docker rm ${JOB_NAME}'
            }
        }

	    stage('Build') {
            steps {
                script {
                    app = docker.build("sit753")
                }
            }
        }

        stage('Test') {
           steps {

                // sh label: '', script: "docker run -d --name ${JOB_NAME} -p 5000:5000 ${img}"
                echo "Test with Selenium..."
          }
        }

        stage('Code Quality Analysis') {
           steps {

                echo "Code Quality with SonarQube..."
          }
        }

        stage('Deploy - Push to ECR') {
            steps {
                script {
                    // Push to AWS ECR
                    docker.withRegistry("${ECR_REPOSITORY}", "ecr:${AWS_DEFAULT_REGION}:aws-credentials") {
                        app.push("${env.BUILD_NUMBER}")
                        app.push("latest")
                    }
                }
            }
        }

        stage('Deploy - Push to AWS Elastic Beanstalk') {
            steps {
                script {
                    // Deploy to AWS Elastic Beanstalk
                    sh "zip -r deployment-package.zip Dockerrun.aws.json"
                    
                    // Create a new application version and update the environment
                    withAWS(credentials: 'aws-credentials', region: "${AWS_DEFAULT_REGION}") {
                        sh "aws s3 cp deployment-package.zip s3://${S3_BUCKET}/${EB_APPLICATION_NAME}-${IMAGE_TAG}.zip"
                        sh "aws elasticbeanstalk create-application-version --application-name ${EB_APPLICATION_NAME} --version-label ${IMAGE_TAG} --source-bundle S3Bucket=${S3_BUCKET},S3Key=${EB_APPLICATION_NAME}-${IMAGE_TAG}.zip"
                        sh "aws elasticbeanstalk update-environment --application-name ${EB_APPLICATION_NAME} --environment-name ${EB_ENVIRONMENT_NAME} --version-label ${IMAGE_TAG}"
                    }
                }
            }
        }
    }
}