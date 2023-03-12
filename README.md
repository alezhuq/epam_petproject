[![Build Status](https://app.travis-ci.com/alezhuq/epam_petproject.svg?branch=develop)](https://app.travis-ci.com/alezhuq/epam_petproject)
[![Coverage Status](https://coveralls.io/repos/github/alezhuq/epam_petproject/badge.svg)](https://coveralls.io/github/alezhuq/epam_petproject) 
[![linting: pylint](https://img.shields.io/badge/linting-pylint-green)](https://github.com/alezhuq/epam_petproject)


design in figma https://www.figma.com/file/P5pIAfoNniwhInVr6liURa/Yezz-katalog?node-id=0%3A1&t=zHOjTyK6Dv1SGfH4-0


Guide
1) clone the project :
git clone https://github.com/alezhuq/epam_petproject
2) always good to check if your dependencies are up to date:
sudo apt-get update
3) install docker and docker-compose :
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
4) run docker containers:
4.1) for the first time:
sudo docker-compose up --build
4.2) if already built:
sudo docker-compose up
#### !important: if you get "permission denied: unknown" on the entrypoint.sh file, run this command
sudo chmod +x entrypoint.sh
#### after launch:
backend will be available at http://localhost:5000/ (you should see {"status": "working"})
frontend will be on http://localhost:3000/

(project was built on 5.18.0-kali7-amd64)
