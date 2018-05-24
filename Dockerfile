FROM tensorflow/tensorflow:latest

LABEL maintainer="Niels Schneider @APG"

WORKDIR /EMODASH

# RUN pip install -r requirements.txt

# Install.
RUN \
  sed -i 's/# \(.*multiverse$\)/\1/g' /etc/apt/sources.list && \
  apt-get update && \
  apt-get -y upgrade && \
  apt-get -y install build-essential && \
  apt-get -y install libmagic-dev && \
  apt-get -y install python-tk



RUN pip --no-cache-dir install \
        keras \
        pymongo \
        flask \
        pyAudioAnalysis \
        pydub
        # python_magic \
        # python-libmagic

COPY ./PythonScripts /EMODASH

EXPOSE 50001

CMD ["python", "FlaskNeuralAnnotator_tf.py"]