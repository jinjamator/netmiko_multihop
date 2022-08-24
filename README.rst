Introduction
==================


netmiko_multihop is an out of tree netmiko monkeypatch which adds multihop capability.


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

    ssh = ConnectHandler(**jumphost1)
    # now we are on jumphost1
    ssh.jump_to(jumphost2).jump_to(target1)
    # now we are on target1
    print(ssh.send_command("show inventory"))
    ssh.jump_back()
    # now we are on jumphost2
    ssh.jump_to(target2)
    print(ssh.send_command("show inventory"))



Contribute
----------

- Issue Tracker: https://github.com/jinjamator/netmiko_multihop/issues
- Source Code: https://github.com/jinjamator/netmiko_multihop

License
-----------------

This project is licensed under the Apache License Version 2.0