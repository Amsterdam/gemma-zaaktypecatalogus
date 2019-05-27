def tryStep(String message, Closure block, Closure tearDown = null) {
    try {
        block()
    }
    catch (Throwable t) {
        slackSend message: "${env.JOB_NAME}: ${message} failure ${env.BUILD_URL}", channel: '#ci-channel', color: 'danger'

        throw t
    }
    finally {
        if (tearDown) {
            tearDown()
        }
    }
}


node {
    stage("Checkout") {
        checkout scm
    }



    stage("Build image") {
        tryStep "build", {
            def image = docker.build("repo.data.amsterdam.nl/gemma-ztc:${env.BUILD_NUMBER}",
                "--build-arg http_proxy=${JENKINS_HTTP_PROXY_STRING} " +
                "--build-arg https_proxy=${JENKINS_HTTP_PROXY_STRING} ."
            )
            image.push()
        }
    }
}



String BRANCH = "${env.BRANCH_NAME}"

if (BRANCH == "master") {

    node {
        stage('Push acceptance image') {
            tryStep "image tagging", {
                def image = docker.image("repo.data.amsterdam.nl/gemma-ztc:${env.BUILD_NUMBER}")
                image.pull()
                image.push("acceptance")
                image.push("production")
            }
        }
    }

    node {
        stage("Deploy to ACC") {
            tryStep "deployment", {
                build job: 'Subtask_Openstack_Playbook',
                        parameters: [
                                [$class: 'StringParameterValue', name: 'INVENTORY', value: 'acceptance'],
                                [$class: 'StringParameterValue', name: 'PLAYBOOK', value: 'deploy-zaaktypecatalogus.yml'],
                        ]
            }
        }
    }


    stage('Waiting for approval') {
        slackSend channel: '#ci-channel-app', color: 'warning', message: 'zaaktypecatalogus is waiting for Production Release - please confirm'
        input "Deploy to Production?"
    }

    node {
        stage('Push production image') {
            tryStep "image tagging", {
                def image = docker.image("repo.data.amsterdam.nl/gemma-ztc:${env.BUILD_NUMBER}")
                image.pull()
                image.push("production")
                image.push("latest")
            }
        }
    }

    node {
        stage("Deploy") {
            tryStep "deployment", {
                build job: 'Subtask_Openstack_Playbook',
                        parameters: [
                                [$class: 'StringParameterValue', name: 'INVENTORY', value: 'production'],
                                [$class: 'StringParameterValue', name: 'PLAYBOOK', value: 'deploy-zaaktypecatalogus.yml'],
                        ]
            }
        }
    }
}
