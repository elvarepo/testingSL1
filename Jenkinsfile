pipeline {
    agent any

    environment {
        APP_DIR = "/home/ec2-user/pet-record-app"
        PID_FILE = "/home/ec2-user/pet-record-app/app.pid"
        LOG_FILE = "/home/ec2-user/pet-record-app/app.log"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build') {
            steps {
                sh '''
                    python3 --version
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                    . venv/bin/activate
                    python3 -c "import app; print('Test passed: app imported successfully')"
                '''
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                    mkdir -p $APP_DIR
                    cp app.py requirements.txt $APP_DIR/

                    cd $APP_DIR
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt

                    if [ -f $PID_FILE ]; then
                      PID=$(cat $PID_FILE)
                      if ps -p $PID > /dev/null 2>&1; then
                        kill $PID || true
                      fi
                      rm -f $PID_FILE
                    fi

                    nohup $APP_DIR/venv/bin/python3 $APP_DIR/app.py > $LOG_FILE 2>&1 &
                    echo $! > $PID_FILE
                '''
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully. App deployed on EC2.'
        }
        failure {
            echo 'Pipeline failed.'
        }
    }
}
