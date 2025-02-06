# bssh
Basic SSH connection manager written in python, zero dependencies.

```sh
+--------+-------------+---------------------+----------+---------------+-------------------+
|   ID   |     name    |        domain       |   port   |      user     |      keyFile      |
+--------+-------------+---------------------+----------+---------------+-------------------+
|   1    |     test    |   test.domain.com   |    22    |      root     |                   |
|   2    |     prod    |    production.com   |    22    |      root     |                   |
|   3    |    local    |     192.168.0.1     |    22    |       bb      |   ~/.ssh/id_rsa   |
|   4    |   staging   |    243.121.191.45   |   2222   |   testerJoe   |                   |
+--------+-------------+---------------------+----------+---------------+-------------------+
Enter the number of the SSH connection you want to connect. CTRL+C to exit. [m] for menu: 
```

The given cicd for the build is producing runnable binary:

    - glibc: debian:buster or any later version of it and ubuntu etc...
    - musl: alpine:3.16 or any later version
