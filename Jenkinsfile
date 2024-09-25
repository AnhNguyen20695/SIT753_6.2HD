pipeline {
    environment {
        registry = ""
        registryCredential = ''
        dockerImage = ''
    }
    options {
        skipStagesAfterUnstable()
    }

    stages {
        // stage('Checkout') {
        //     steps {
        //         git 'https://github.com/AnhNguyen20695/SIT753_6.2HD.git'
        //     }
        // }

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
                    img = registry + ":${env.BUILD_ID}"
                    println ("${img}")
                    dockerImage = docker.build("${img}")
                }
            }
        }

        stage('Test') {
           steps {

                sh label: '', script: "docker run -d --name ${JOB_NAME} -p 5000:5000 ${img}"
          }
        }

        stage('Code Quality Analysis') {
           steps {

                echo "Code Quality with SonarQube.."
          }
        }

        stage('Deploy') {
            steps {
                script {
                    docker.withRegistry( '277707121057.dkr.ecr.ap-southeast-2.amazonaws.com/sit753', 'ecr:ap-southeast-2:aws-credentials' ) {
                        dockerImage.push("${env.BUILD_NUMBER}")
                        dockerImage.push("latest")
                    }
                }
            }
        }
    }
}