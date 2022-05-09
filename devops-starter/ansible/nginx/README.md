Ansible Version 2.5

To start testing ansible, first provision a vagrant box
for host or control machine for the node
*make sure ssh or sshd is enabled on hosts or remote*

	$ sudo systemctl enable sshd
	$ sudo systemctl start sshd
### See the vagrant guide
### generate first your ssh keys
	$ ssh-keygen -t rsa
### copy public key to host machine(node)
	$ ssh-copy-id -i user/root@ip
	or 
	ssh-copy-id user@hostname.example.com
### Install ansible through pip or a package manager, in this guide ansible is installed with pip
### Host and nodes are using archlinux distro
### Make sure nodes already have python installed
### Update or include updating the host in your plays before executing more complex commands

### To gather facts about remote

	$ ansible all -m setup -a 'filter=ansible_distribution' 

### Create/Edit the inventory file which contain ip addresses of your nodes and the ansible.cfg for ansible configurations

### Test node with, test-servers are list of host set on host file
	
	$ ansible test-servers -m ping 

### To create a playbook, create a file with .yml as extension

### Visit the docs for more info on plays, task, modules and handlers

### Sample running of playbook
	$ ansible-playbook 'yourplaybook.yml'

### Check sample playbook that installs nginx on target node

### See also roles to organize more complex playbooks

### Bootstrap  roles
	$ mkdir roles && cd roles
	$ ansible-galaxy init <role-name>
### Running a playbook
	$ ansible-playbook <host> <playbook>


### Other commands
### Run against localhost
	$ ansible -i ./hosts --connection=local local -m ping

### Run against remote server
	$ ansible -i ./hosts remote -m ping

### Enable log in
	$ ansible -i ./hosts --ask-pass --ssh-extra-args='-o "PubkeyAuthentication=no"' all -m ping.

### Explained

-i ./hosts - set inventory file
remote, local, all - the host you want to run insides hosts file.
-m ping - Use the "ping" module.
-c local | --connection=local - Run commands on the local server, not over SSH

### Using ansible vault

### Encrypting files
	$ ansible-vault encrypt file1 file2 ...

### Decrypting  files
	$ ansible-vault decrypt file1 file2 ...

### Change password
	$ ansible-vault rekey file1 file2 ...

### View without editing
	$ ansible-vault view file
	
### Run playbook with pass
	$ ansible-playbook --ask-vault-pass playbook.yml
