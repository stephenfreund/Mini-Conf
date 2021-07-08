FROM mcr.microsoft.com/vscode/devcontainers/python:3.9

# Use this user and group inside the devcontainer
ARG USERNAME=mycode
ARG USER_ID
ARG GROUP_ID

RUN addgroup --gid $GROUP_ID $USERNAME
RUN adduser --disabled-password --gecos '' --uid $USER_ID --gid $GROUP_ID $USERNAME

# Install mini-conf dependencies from pip
RUN pip install --force-reinstall -Iv \
    certifi==2020.12.5 \
    chardet==4.0.0 \
    click==7.1.2 \
    Flask==1.1.2 \
    Flask-Markdown==0.3 \
    Frozen-Flask==0.15 \
    idna==2.10 \
    itsdangerous==1.1.0 \
    Jinja2==2.11.3 \
    Markdown==3.3.3 \
    MarkupSafe==1.1.1 \
    numpy==1.20.1 \
    pandas==1.2.2 \
    python-dateutil==2.8.1 \
    pytz==2021.1 \
    PyYAML==5.4.1 \
    requests==2.25.1 \
    six==1.15.0 \
    tqdm==4.57.0 \
    urllib3==1.26.3 \
    Werkzeug==1.0.1

# Install emacs
RUN apt-get update \
    && apt-get install -y emacs-nox

# Create a .bashrc with a welcome message
RUN echo '\n\
echo\n\
echo Welcome to PLDI Mini-Conf.  Type \"make run\" to start the server.\n\
echo\n'\
>> /etc/bash.bashrc

# Switch to non-root user
USER $USERNAME