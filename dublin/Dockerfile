FROM python:3.14-slim
RUN pip install --no-cache-dir jupyterlab anthropic clear-html dateparser extruct html-text \
    lxml parsel price-parser w3lib zyte-parsers
WORKDIR /workshop
COPY . .
EXPOSE 8888
# Token disabled: the port is only published on 127.0.0.1 (see docker-compose.yml)
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--no-browser", "--allow-root", "--ServerApp.token=", "--ServerApp.password=", "--ServerApp.root_dir=/workshop", "--LabApp.default_url=/lab/tree/demo/01_parsing.ipynb"]
