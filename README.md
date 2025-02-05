# bssh
Basic SSH connection manager written in python, zero dependencies.

The given cicd for the build is producing runnable binary:

    - glibc: debian:bullseye or any later version of it and ubuntu etc...
    - musl: alpine:3.16 or any later version

Known bugs / missing features:

    - The whole edit/update feature is missing
    - Adding new record, and ctrl+c any fields result an error, need to implement better error handling.
    - When there is no record, ctrl+c giving error.