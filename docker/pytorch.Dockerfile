FROM nvcr.io/nvidia/pytorch:20.06-py3

WORKDIR /usr/src/butterfly

COPY . .

RUN pip install -e .[all]

CMD [ "/bin/bash" ]

