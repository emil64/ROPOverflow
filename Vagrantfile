Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/bionic64"
  config.vm.synced_folder ".", "/home/vagrant/s3/"
  config.vm.provider "virtualbox" do |v|
    v.name = "S3_CW_Project4"
  end
  config.vm.provision "shell", inline: <<-SHELL
    sudo apt-get update
    sudo apt-get install -y python3-pip gcc-multilib gdb
    pip3 install pygdbmi
    pip3 install ropgadget
    wget https://cs-uob.github.io/COMSM0049/code/nc071.tar.gz
    tar -xvf nc071.tar.gz
    cd netcat-0.7.1/
    ./configure
    make
    cp src/netcat /tmp/nc
  SHELL
end