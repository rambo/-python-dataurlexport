=============
dataurlexport
=============

Post-process RUNE outputs and export data urls as files


Docker
------

For more controlled deployments and to get rid of "works on my computer" -syndrome, we always
make sure our software works under docker.

It's also a quick way to get started with a standard development environment.

SSH agent forwarding
^^^^^^^^^^^^^^^^^^^^

We need buildkit_::

    export DOCKER_BUILDKIT=1

.. _buildkit: https://docs.docker.com/develop/develop-images/build_enhancements/

And also the exact way for forwarding agent to running instance is different on OSX::

    export DOCKER_SSHAGENT="-v /run/host-services/ssh-auth.sock:/run/host-services/ssh-auth.sock -e SSH_AUTH_SOCK=/run/host-services/ssh-auth.sock"

and Linux::

    export DOCKER_SSHAGENT="-v $SSH_AUTH_SOCK:$SSH_AUTH_SOCK -e SSH_AUTH_SOCK"

Creating a development container
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Build image, create container and start it::

    docker build --ssh default --target devel_shell -t dataurlexport:devel_shell .
    docker create --name dataurlexport_devel -v "$(pwd):/app" -it $(echo $DOCKER_SSHAGENT) dataurlexport:devel_shell
    docker start -i dataurlexport_devel

pre-commit considerations
^^^^^^^^^^^^^^^^^^^^^^^^^

If working in Docker instead of native env you need to run the pre-commit checks in docker too::

    docker exec -i dataurlexport_devel /bin/bash -c "pre-commit install --install-hooks"
    docker exec -i dataurlexport_devel /bin/bash -c "pre-commit run --all-files"

You need to have the container running, see above. Or alternatively use the docker run syntax but using
the running container is faster::

    docker run --rm -it -v "$(pwd):/app" dataurlexport:devel_shell -c "pre-commit run --all-files"

Test suite
^^^^^^^^^^

You can use the devel shell to run py.test when doing development, for CI use
the "tox" target in the Dockerfile::

    docker build --ssh default --target tox -t dataurlexport:tox .
    docker run --rm -it -v "$(pwd):/app" $(echo $DOCKER_SSHAGENT) dataurlexport:tox

Production docker
^^^^^^^^^^^^^^^^^

There's a "production" target as well for running the application, remember to change that
architecture tag to arm64 if building on ARM::

    docker build --ssh default --target production -t dataurlexport:latest .
    docker run -it --name dataurlexport dataurlexport:amd64-latest

Development
-----------

TLDR:

- Create and activate a Python 3.13 virtualenv (assuming virtualenvwrapper)::

    mkvirtualenv -p $(which python3.13) my_virtualenv

- change to a branch::

    git checkout -b my_branch

- install Poetry: https://python-poetry.org/docs/#installation
- Install project deps and pre-commit hooks::

    poetry install
    git add poetry.lock
    pre-commit install --install-hooks
    pre-commit run --all-files

If you get weird errors about missing packages from pre-commit try running it with "poetry run pre-commit".

- Ready to go.

Remember to activate your virtualenv whenever working on the repo, this is needed
because pylint and mypy pre-commit hooks use the "system" python for now (because reasons).

Running "pre-commit run --all-files" and "py.test -v" regularly during development and
especially before committing will save you some headache.
