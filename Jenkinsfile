pipeline {
    agent any

    environment {
        REPORT_DIR = "allure-results"
    }

    stages {
//         stage('拉取代码') {
//             steps {
//                 git branch: 'main', url: 'https://github.com/example/api-test.git'
//             }
//         }
//
//         stage('启动测试环境') {
//             steps {
//                 sh 'docker-compose up -d'
//             }
//         }

        stage('执行UI测试') {
            steps {
//                 sh 'docker run --rm -v $WORKSPACE:/app python:3.9 bash -c "pip install -r /app/requirements.txt && pytest /app/tests --alluredir=${REPORT_DIR}"'
                python3.8 -m pytest
            }
        }

//         stage('生成测试报告') {
//             steps {
//                 sh 'allure generate ${REPORT_DIR} -o allure-report --clean'
//             }
//         }

        stage('存档并发送通知') {
            steps {
//                 archiveArtifacts artifacts: 'allure-report/**', fingerprint: true
                mail to: 'mforward@126.com',
                     subject: "接口测试报告",
//                      body: "接口测试完成，请查看测试报告: ${BUILD_URL}/allure-report"
                     body: "接口测试完成，请查看测试报告:"
            }
        }

//         stage('关闭测试环境') {
//             steps {
//                 sh 'docker-compose down'
//             }
//         }
    }
}

