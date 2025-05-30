pipeline {
//     environment {
//         PATH = "/usr/local/bin:"
//     }
    agent any
//     {
//         docker {
//             image 'python:3.8'  // 运行 Python 3.8 Docker 镜像
//             args '-v $PWD:/app -w /app'  // 挂载当前目录到 Docker 并设置工作目录
//         }
//     }

    stages {
//         stage('下载python依赖包') {
//             steps {
//                 sh 'pip install --no-cache-dir -r requirements.txt'  // 安装 Python 依赖
//             }
//         }
        stage('执行测试') {
            steps {
                        sh '/Library/Frameworks/Python.framework/Versions/3.8/bin/python3.8 -m pytest'
            }
        }
    }
    post {
        always {
            script {
                if (fileExists('reports/')) {
                    echo "✅ 归档测试报告"
                    archiveArtifacts artifacts: 'reports/**', fingerprint: true
                } else {
                    echo "⚠️ 测试报告不存在，跳过归档"
                }
            }

            // 生成 Allure 报告
            allure([
                includeProperties: false,
                jdk: '',
                reportBuildPolicy: 'ALWAYS',
                results: [[path: 'reports/']]
            ])
        }
    }
}