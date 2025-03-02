pipeline {
    agent {
        docker {
            image 'python:3.8'  // 运行 Python 3.8 Docker 镜像
            args '-v $PWD:/app -w /app'  // 挂载当前目录到 Docker 并设置工作目录
        }
    }

    stages {
        stage('下载python依赖包') {
            steps {
                sh 'pip install --no-cache-dir -r requirements.txt'  // 安装 Python 依赖
            }
        }
        stage('执行测试') {
            steps {
                sh 'pytest'  // 运行 pytest 测试
            }
        }
    }
}