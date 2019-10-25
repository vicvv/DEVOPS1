vagrant up --no-provision
vagrant provision --provision-with coreinstall
vagrant provision --provision-with installxrdp
vagrant provision --provision-with installxfce
vagrant provision --provision-with installvscode
vagrant provision --provision-with reboot