FROM jenkins/jenkins:lts

USER root

RUN apt-get update -y \
	&& apt-get upgrade -y \
	&& DEBIAN_FRONTEND=noninteractive apt-get install -y \
		apt-transport-https \
		ca-certificates \
		curl \
		gnupg2 \
		software-properties-common \
	&& curl -fsSL https://download.docker.com/linux/debian/gpg | \
		apt-key add - \
	&& add-apt-repository \
		"deb [arch=amd64] https://download.docker.com/linux/debian \
		$(lsb_release -cs) \
		stable" \
	&& apt-get update \
	&& DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
		docker-ce \
	&& usermod -aG docker jenkins \
	&& rm -rf /var/lib/apt/lists/* \
	&& apt-get clean

USER jenkins

ENTRYPOINT [ "/sbin/tini", "--", "/usr/local/bin/jenkins.sh" ]

