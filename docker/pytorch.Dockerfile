FROM nvcr.io/nvidia/pytorch:19.12-py3

WORKDIR /usr/src/butterfly

COPY . .

RUN pip install -e .[all]

CMD [ "/bin/bash" ]

