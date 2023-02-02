Vagrant.configure("2") do |config|
    servers=[
        {
          :hostname => "control",
          :box => "bento/ubuntu-18.04",
          :ip => "172.16.7.100",
          :ssh_port => '6666'
        },
        {
          :hostname => "node1",
          :box => "bento/ubuntu-18.04",
          :ip => "172.16.7.101",
          :ssh_port => '6667'
        },
        {
          :hostname => "node2",
          :box => "bento/ubuntu-18.04",
          :ip => "172.16.7.102",
          :ssh_port => '6668'
        },
        {
          :hostname => "node3",
          :box => "bento/ubuntu-18.04",
          :ip => "172.16.7.103",
          :ssh_port => '6669'
        }
      ]

    servers.each do |machine|
        config.vm.define machine[:hostname] do |node|
            node.vm.box = machine[:box]
            node.vm.hostname = machine[:hostname]
            node.vm.network :private_network, ip: machine[:ip]
            node.vm.network "forwarded_port", guest: 22, host: machine[:ssh_port], id: "ssh"
            node.vm.provider :virtualbox do |vb|
                vb.customize ["modifyvm", :id, "--memory", 512]
                vb.customize ["modifyvm", :id, "--cpus", 1]
            sudo cp hosts /et hosts
            end
        end
    end
end