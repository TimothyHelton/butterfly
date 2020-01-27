FROM pytorch/pytorch

WORKDIR /usr/src/butterfly

COPY . .

RUN conda update -y conda \
	&& conda update -y --all \
	&& while read requirement; do conda install --yes ${requirement}; done < requirements.txt \
	&& conda install -y pytorch torchvision -c pytorch \
	&& pip install -e .[build,data,database,docs,notebook,profile,test] \
	&& curl -sL https://deb.nodesource.com/setup_11.x | bash - \
	&& apt-get update -y \
	&& apt-get upgrade -y \
	&& apt-get install -y \
		apt-utils \
		nodejs \
	&& jupyter labextension install @telamonian/theme-darcula \
	&& jupyter labextension install jupyterlab-drawio \
	# && jupyter labextension install jupyterlab-plotly \
	# && jupyter labextension install jupyterlab-toc \
	&& rm -rf /tmp/* \
	&& rm -rf /var/lib/apt/lists/* \
	&& apt-get clean

CMD [ "/bin/bash" ]

