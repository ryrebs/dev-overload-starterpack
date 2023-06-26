### Explanation on basic commands

    $vagrant init - generates a Vagrantfile that describes the setup of your vagrant box, modify as necessary.
    $vagrant up - turns on your vagrant box.
    $vagrant halt - powers off
    $vagrant suspend - saves the state of your vagrant box
    $vagrant ssh - log in to your vagrant box through ssh
    $vagrant destroy - destroy the box environment, back to the base state

## Creating a box

_Named precise32 from its url_

1. vagrant init precise32 http://files.vagrantup.com/precise32.box

**or**

Without knowing the url repo
$ vagrant init `vboxname in vagrant repo`

_Modify vagrantfile as needed_

2. vagrant up - run the machine, download if it doesn't exist

3. vagrant ssh after downloading, login by

### Notes:

**Create a separate folder since the path where vagrantfile is created is shared in the box**

_Check the documentation for more details_

---

## Creating a custom box

1. Create a virtual machine of your choice. In this example
   will be using ubuntu server 16.04 on virtualbox

Example settings:

    Name: vagrant-ubuntu64
    Type: Linux
    Version: Ubuntu64
    Memory Size: 512MB
    New Virtual Disk: [Type: VMDK, Size: 40 GB]


    Disable audio
    Disable USB
    Ensure Network Adapter 1 is set to NAT
    Add this port-forwarding rule:
     [Name: SSH, Protocol: TCP, Host IP: blank, Host Port: 2222, Guest IP: blank, Guest Port: 22]

2.  Once installation is finished, change root pass

    $ su -

    $ sudo passwd root

3.  Setup vagrant user to run sudo without prompting pass

    a. $ sudo visudo -f /etc/sudoers.d/vagrant

    b. Add this line : vagrant ALL=(ALL) NOPASSWD:ALL

4.  Update the os and restart

    $ sudo apt-get update -y

    $ sudo apt-get upgrade -y

    $ sudo shutdown -r now

5.  Install the unsecure vagrant key

    $ mkdir -p /home/vagrant/.ssh

    $ chmod 0700 /home/vagrant/.ssh

    $ wget --no-check-certificate \
     https://raw.github.com/mitchellh/vagrant/master/keys/vagrant.pub \
     -O /home/vagrant/.ssh/authorized_keys

    $ chmod 0600 /home/vagrant/.ssh/authorized_keys

    $ chown -R vagrant /home/vagrant/.ssh

6.  Uncomment `AuthorizedKeysFile %h/.ssh/authorized_keys` on /etc/ssh/sshd_config
7.  Install linuxheaders

    $ sudo apt-get install -y gcc build-essential dkms

    - Should install `linux-headers-server`
      1/10/2019 can't find package using ubuntu 16.04 lts
      perhaps a workaround \*

    ( $ sudo apt-get upgrade linux-generic linux-headers-generic linux-image-generic )

8.  Install vbox GuestAdditions

    $ sudo mount /dev/cdrom /mnt

    $ cd /mnt

    $ sudo ./VBoxLinuxAdditions.run

9.  Zeroing the drive first before packaging

    $ sudo dd if=/dev/zero of=/EMPTY bs=1M

    $ sudo rm -f /EMPTY

10. Package the box with:

    $ vagrant package --base `name of your created vbox(vagrant-ubuntu-server)`

11. Add a packaged box to vagrant environment

    a. adds a box based from a local packaged box or remote box

    b. and a new box file in .vagrant.d/boxes

        $ vagrant box add `box name` `your packaged box url`

    c. configure the box

        $ vagrant init `box name`
        $ vagrant up
        $ vagrant ssh # to login

---

## Cloning

By cloning you maintain a clean slate copy and have another copy or more for experiments.

A. By halting the current box and packaging it. Navigate in the vagrant folder where the vagrant box is

    	1. create a package.box

    		$ vagrant halt

    		$ vagrant package

    	2. proceed to step 11 or configure it manually by:

    		1. $ vagrant init

    		2. edit this line with the generated vagrant file

    			config.vm.box = "your-box-name"

    			   config.vm.box_url = "file:///location-of-the-box"

    			 *edit ip or others ...

    		3. $ vagrant up

    		4. $ vagrant ssh

B. Creating directly from the packaged box using step 11 above

**Note**

1. Cloning by halting makes you copy a box after a user has installed packages

2. Cloning a packaged box creates a base without installed packages
