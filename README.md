# DevOps-Practice
DevOps Practice with Vagrant, Ansible, Docker and Container Orchestration

In this Project introduce the concept of configuration as code with Vagrant and VirtualBox, go over configuration management with Ansible, then Containers and Container Orchestration with Docker and Docker Swarm.

# Vagrant Cheatsheet
https://gist.github.com/wpscholar/a49594e2e2b918f4d0c4

# Install Vagrant
https://www.vagrantup.com/docs/installation

# Usage
1. Up with Vagrant
```
vagrant up
vagrant ssh
sudo cp hosts /etc/hosts
```
2. We check if everything is OK
```
ssh vagrant@node1
```
3. Make hosts SSH accessible /on the control station/
```
ssh-keygen
ssh-copy-id node1 && ssh-copy-id node2 && ssh-copy-id node3
```
4. Install Ansible on control station
```
sudo apt-get install ansible -y
```
5. Test ansible
```
cd Ansible/
ansible nodes -i myhosts -m command -a hostname
```
6. Install Python on all nodes
```
####ansible nodes -i myhosts -m command -a 'sudo apt-get -y install python-simplejson'
```
7. Run the playbook to install docker
```
ansible-playbook -i myhosts -K playbook.yml
```
