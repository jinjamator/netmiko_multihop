Introduction
==================


netmiko_multihop is an out of tree netmiko monkeypatch which adds multihop capability. 
Currently following platforms are supported as intermediate hop:
    - linux
    - cisco_nxos
    - cisco_ios
Other platforms can be added easily if required.


Installation
------------

Install the netmiko_multihop package by running:

    pip3 install netmiko-multihop

Usage
-----

.. code-block:: python

    import  netmiko_multihop
    from netmiko import ConnectHandler


    jumphost1 = {
        'device_type': 'linux',
        'ip': <ip_jumphost1>,
        'username': <ssh_username_jumphost1>,
        'password': <ssh_password_jumphost1>,
        'port': 22,
    }

    jumphost2 = {
        'device_type': 'linux',
        'ip': <ip_jumphost2>,
        'username': <ssh_username_jumphost2>,
        'password': <ssh_password_jumphost2>,
        'port': 22,
    }

    target1 = {
        'device_type': 'cisco_nxos',
        'ip': <ip_target1>,
        'username': <ssh_username_target1>,,
        'password': <ssh_password_target1>,
        'port': 22,
    }

    target2 = {
        'device_type': 'cisco_ios',
        'ip': <ip_target2>,
        'username': <ssh_username_target2>,
        'password': <ssh_password_target2>,
        'port': 22,
    }

    # If the next hop is reachable via vrf on the current hop, add the vrf parameter to the destination configuration.
    # Eg.: Target1 is reachable via vrf mgmt from target2. You want to jump from target1 to target2. Add the parameter vrf to target2 before you jump from target1 to target2.

    ssh = ConnectHandler(**jumphost1)
    # now we are on jumphost1
    # this is where the magic starts. as jump_to returns the object instance we can jump multiple hops at once

    ssh.jump_to(**jumphost2).jump_to(**target1)
    # now we are on target1
    print(ssh.send_command("show inventory"))
    # lets get back a single jump 
    ssh.jump_back()
    # now we are on jumphost2
    ssh.jump_to(**target2)
    # now we are on target2
    print(ssh.send_command("show inventory"))
    ssh.jump_back()



Contribute
----------

- Issue Tracker: https://github.com/jinjamator/netmiko_multihop/issues
- Source Code: https://github.com/jinjamator/netmiko_multihop

License
-----------------

This project is licensed under the Apache License Version 2.0