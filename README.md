# DevOps-Practice
DevOps Practice with Vagrant, Ansible, Docker and Container Orchestration

In this Project introduce the concept of configuration as code with Vagrant and VirtualBox, go over configuration management with Ansible, then Containers and Container Orchestration with Docker and Docker Swarm.

# Vagrant Cheatsheet
https://gist.github.com/voiz80/48bc7edad27d68ac28c148285666a013

# Install Vagrant
https://www.vagrantup.com/docs/installation

# Usage
1. Up with Vagrant
```
vagrant up
vagrant ssh control
@control:~$ cd /vagrant
@control:/vagrant$ sudo cp hosts /etc/hosts
```
2. We check if everything is OK
```
@control:/vagrant$ ssh vagrant@node1
@node1:~$ exit
```
3. Make hosts SSH accessible /on the control station/
```
@control:/vagrant$ ssh-keygen
@control:/vagrant$ ssh-copy-id node1 && ssh-copy-id node2 && ssh-copy-id node3
```
4. Install Ansible on control station
```
@control:/vagrant$ sudo apt-get install ansible -y
```
5. Test ansible
```
@control:/vagrant$ cd Ansible
@control:/vagrant/Ansible$ ansible nodes -i myhosts -m command -a hostname
```
6. Run the playbook to install Python and Docker
```
@control:/vagrant/Ansible$ ansible-playbook -i myhosts -K playbook.yml
```
7. Test docker-compose app
```
@control:/vagrant/Ansible$ ssh vagrant@node1
@node1~$ cd /vagrant/Docker
@node1:/vagrant/Docker$ docker-compose up -d
```
# Troubleshooting
Sometimes if you made a mistake, you made have to re-do the image build with docker-compose build
```
docker-compose build
```
And then from "control" instance:
```
@control:~$ curl node1:5000
```
If it is OK! /Hello User! My container ID: <Container Id >/
```
@node1:/vagrant/Docker$ docker-compose down
```
8. Clone the ansible project in control instance
```
@ncontrol:/vagrant$ git clone https://github.com/voiz80/ansible-swarm-playbook.git
```
*Note I change eth0 to eth1 in this swarm.yml, since ip address didn't match.
```
@control:/vagrant$ cd ansible-swarm-playbook/
@control:/vagrant/ansible-swarm-playbook/$ cp ../Ansible/myhosts myhosts
```
We append multiple lines to file: myhosts
```
@control:/vagrant/ansible-swarm-playbook/$ echo -e "\n[manager] \nnode1 \n[worker] \nnode2 \nnode3" >> myhosts
```
9. And again Run the playbook for Docker Swarm setup... /install all nodes and setup and evryone joined to the cluster/
```
@control:/vagrant/ansible-swarm-playbook/$ ansible-playbook -i myhosts -K swarm.yml
```
10. Verify docker swarm is setup.
```
@control:/vagrant/ansible-swarm-playbook/$ ssh vagrant@node1
@node1:~$ docker node ls
```
We have three nodes in the cluster with node1 Leader!

11. Migrate your app
 - modify docker-compose file to use image instead of build! In this case: "build: ." change with" "image: flask_app:1.0" and RUN ...
 Make image and  export ...
 ```
 @node1:/vagrant/Docker$ docker image  build -t flask_app:1.0 .
 @node1:/vagrant/Docker$ docker save -o flask_app.tar flask_app:1.0
 ```
 In our case we no DockerHubfrom then from control instance we need to ssh node2 and node3 to load flask_app image: ssh vagrant@node2 and ssh vagrant@node3
 ``` 
    @node2:~$ cd /vagrant/Docker && docker load -i flask_app.tar
    @node3:~$ cd /vagrant/Docker && docker load -i flask_app.tar
```
```
 @node1:/vagrant/Docker$ docker stack deploy --compose-file docker-compose.yml myapp
 ```

 ```
@node1:/vagrant/Docker$ docker stack ls
@node1:/vagrant/Docker$ docker stack services myapp
```
And replicate all nodes ...
```
@node1:/vagrant/Docker$ docker service scale myapp_web=6
```
And let's see what we've done ...
```
@node1:/vagrant/Docker$ docker service ls

Output:
ID             NAME        MODE         REPLICAS   IMAGE               PORTS
xq139kazq7lm   myapp_web   replicated   6/6        docker_web:latest   *:5000->5000/tcp

@node1:/vagrant/Docker$ docker service ps myapp_web

Output:
ID             NAME          IMAGE           NODE      DESIRED STATE   CURRENT STATE                ERROR     PORTS
xzi8jeiv5vuq   myapp_web.1   flask_app:1.0   node1     Running         Running about a minute ago             
qycgv85p9u7s   myapp_web.2   flask_app:1.0   node3     Running         Running 39 seconds ago                 
4cbxsoxvml76   myapp_web.3   flask_app:1.0   node1     Running         Running 40 seconds ago                 
stvkc30lnru6   myapp_web.4   flask_app:1.0   node2     Running         Running 39 seconds ago                 
skci17834hik   myapp_web.5   flask_app:1.0   node2     Running         Running 39 seconds ago                 
co4lulgjtnt2   myapp_web.6   flask_app:1.0   node3     Running         Running 39 seconds ago  
```

12. Now test load balancing 
controll instance: 
```
@control:~$ watch -n 0.9 "curl node1:5000"
```
We achieved load balancing between 6 replicated containers!
