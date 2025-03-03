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
                try {
                        sh '/Library/Frameworks/Python.framework/Versions/3.8/bin/python3.8 -m pytest'
                    } catch (Exception e) {
                        echo "⚠️ pytest 失败，但继续执行"
                    }
            }
        }
        stage('Archive Test Results') {
            steps {
                echo "归档 Allure 测试报告..."
                archiveArtifacts artifacts: 'reports/**', fingerprint: true
            }
    }
    }

}