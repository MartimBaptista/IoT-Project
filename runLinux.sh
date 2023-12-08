#print to console advising we will be freeing a port for our app
echo "We will be shutting down a program running on port 5432, beware"
sudo kill -9 $(sudo lsof -ti:5432)
docker-compose -f cloud-Infrastructure/docker-compose.yml up