git pull
docker build . -t utda/sim_gaikotsu:1.0
docker stop sim_gaikotsu
docker rm sim_gaikotsu
docker run --name sim_gaikotsu -itd -p 8027:5002 utda/sim_gaikotsu:1.0
