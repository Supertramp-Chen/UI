pipeline {
    agent { label 'master' }  // 让 Jenkins 任务只在当前服务器（Master 节点）运行


    stages {
        stage('启动 Docker 运行环境') {
            steps {
                sh 'docker-compose up -d'  // 启动 Python 运行环境和 Allure
            }
        }

        stage('安装依赖') {
            steps {
                sh 'docker exec python-runner pip install -r /app/requirements.txt'
            }
        }

        stage('执行 API 测试') {
            steps {
                sh 'docker exec python-runner pytest '
            }
        }

//         stage('生成 Allure 报告') {
//             steps {
//                 sh 'docker exec allure-server allure generate /app/allure-results -o /app/allure-report --clean'
//             }
//         }
//
//         stage('存档并发布 Allure 报告') {
//             steps {
//                 archiveArtifacts artifacts: 'allure-report/**', fingerprint: true
//                 echo "Allure 报告地址: http://服务器IP:5050"
//             }
//         }

        stage('关闭 Docker 运行环境') {
            steps {
                sh 'docker-compose down'  // 释放 Docker 资源
            }
        }
    }
}