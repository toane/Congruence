#! /bin/bash
CONG_PATH="/home/mathias/bigdata/projet/Congruence"

MONGO_PATH=$CONG_PATH"/ressources/mongo"
xfce4-terminal -T MONGO \
	       --default-working-directory=$MONGO_PATH \
	       -x ./mongo_launch.sh

NLP_PATH=$CONG_PATH"/ressources/coreNLP"
xfce4-terminal -T CoreNLP \
	       --default-working-directory=$NLP_PATH \
	       -x ./servers_launch.sh

xfce4-terminal -T FLASK \
	       -x ./run_flask.sh
