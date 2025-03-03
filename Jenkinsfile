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
                sh '/Library/Frameworks/Python.framework/Versions/3.8/bin/python3.8 -m pytest'  // 运行 pytest 测试
            }
        }
    }
    post {
        success {
            dingTalk (
                robot: "YOUR_DINGTALK_ROBOT",
                type: "MARKDOWN",
                title: "🎉 Jenkins 构建成功",
                text: "**Jenkins 构建成功**\n\n"
                    + "> **任务**: ${env.JOB_NAME}\n"
                    + "> **编号**: ${env.BUILD_NUMBER}\n"
                    + "> **详情**: [点击查看](${env.BUILD_URL})\n"
            )
        }
        failure {
            dingTalk (
                robot: "YOUR_DINGTALK_ROBOT",
                type: "MARKDOWN",
                title: "❌ Jenkins 构建失败",
                text: "**Jenkins 构建失败** 🚨🚨🚨\n\n"
                    + "> **任务**: ${env.JOB_NAME}\n"
                    + "> **编号**: ${env.BUILD_NUMBER}\n"
                    + "> **详情**: [点击查看](${env.BUILD_URL})\n"
                    + "> **请尽快检查错误日志！**"
            )
        }
        unstable {
            dingTalk (
                robot: "YOUR_DINGTALK_ROBOT",
                type: "MARKDOWN",
                title: "⚠️ Jenkins 构建不稳定",
                text: "**Jenkins 构建不稳定** ⚠️⚠️⚠️\n\n"
                    + "> **任务**: ${env.JOB_NAME}\n"
                    + "> **编号**: ${env.BUILD_NUMBER}\n"
                    + "> **详情**: [点击查看](${env.BUILD_URL})\n"
                    + "> **请检查测试用例或代码质量！**"
            )
        }
    }
}