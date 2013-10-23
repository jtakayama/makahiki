# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  # Configuration settings for vagrant-vbguest, based on the vagrant-vbguest Readme.md:
  # vbguest will try to autodetect the path to the VBoxGuestAdditions.iso file.
  # If the path cannot be detected or is in a non-default location, use:
  # config.vbguest.iso_path = "#{ENV['HOME']}/Downloads/VBoxGuestAdditions.iso"
  # or
  # config.vbguest.iso_path = "http://company.server/VirtualBox/%{version}/VBoxGuestAdditions.iso"

  # set auto_update to false, if you do NOT want to check the correct additions 
  # version when booting this machine
  config.vbguest.auto_update = false

  # "true" means vbguest will not download the iso file from a webserver
  config.vbguest.no_remote = true
 
  # Configuration settings for the virtual machine
  config.vm.box = "precise32"
  config.vm.provision :shell, :path => "run_bootstrap.sh"
  # Configures this virtual machine to use a private (host-only) network in 
  # the 192.168.56.0/24 range.
  config.vm.network :private_network, ip: "192.168.56.4"
  config.vm.provider :virtualbox do |vb|
    vb.customize ["modifyvm", :id, "--memory", 1536]
  end
end