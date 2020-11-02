#!/data/data/com.termux/files/usr/bin/bash
if [ ! -f "export.sh" ] ; then
cat <<EOF >export.sh
#!/data/data/com.termux/files/usr/bin/bash
export RUN_FILEBROWSER="true"
export FILEBROWSER_PORT="9998"
export OS_PREFIX="LinuxArm"
export FILEBROWSER_BASEURL="/filebrowser"
export SJVA_RUNNING_TYPE="termux"
EOF
fi

if [ -f "export.sh" ] ; then
    echo "Run export.sh start"
    chmod 777 export.sh
    source export.sh
    echo "Run export.sh end"
fi

if [ "${RUN_FILEBROWSER}" == "true" ] && [ -f ./bin/${OS_PREFIX}/filebrowser ]; then
    chmod +x ./bin/${OS_PREFIX}/filebrowser
    if [ -z "${FILEBROWSER_BASEURL}" ]; then
        nohup ./bin/${OS_PREFIX}/filebrowser -a 0.0.0.0 -p ${FILEBROWSER_PORT} -r / -d ./data/db/filebrowser.db > /dev/null 2>&1 &
    else
        nohup ./bin/${OS_PREFIX}/filebrowser -a 0.0.0.0 -p ${FILEBROWSER_PORT} -r / -d ./data/db/filebrowser.db -b ${FILEBROWSER_BASEURL} > /dev/null 2>&1 &
    fi
    echo "Start Filebrowser. port:${FILEBROWSER_PORT}"
fi

COUNT=0
while [ 1 ];
do
    find . -name "index.lock" -exec rm -f {} \;
    git reset --hard HEAD
    git pull
    chmod 777 .
    chmod -R 777 ./bin

    if [ ! -f "./data/db/sjva.db" ] ; then
        python3 sjva.py 0 ${COUNT} init_db
    fi

    python3 sjva.py 0 ${COUNT} no_celery
    
    RESULT=$?
    echo "PYTHON EXIT CODE : ${RESULT}.............."
    if [ "$RESULT" = "0" ]; then
        echo 'FINISH....'
        break
    else
        echo 'REPEAT....'
    fi 
    COUNT=`expr $COUNT + 1`
done 

ps -eo pid,args | grep filebrowser | grep -v grep | awk '{print $1}' | xargs -r kill -9
