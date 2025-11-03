# Use the Jenkins image with a stable JDK version
FROM jenkins/jenkins:lts-jdk17

# Switch to root user to install dependencies
USER root

# Install prerequisites and Docker
RUN apt-get update -y && \
    apt-get install -y apt-transport-https ca-certificates curl gnupg lsb-release && \
    mkdir -p /etc/apt/keyrings && \
    curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg && \
    echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian bookworm stable" > /etc/apt/sources.list.d/docker.list && \
    apt-get update -y && \
    apt-get install -y docker-ce docker-ce-cli containerd.io && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Add Jenkins user to Docker group
RUN groupadd -f docker && usermod -aG docker jenkins

# Create Docker directory and mountable volume
RUN mkdir -p /var/lib/docker
VOLUME /var/lib/docker

# Switch back to Jenkins user
USER jenkins
    