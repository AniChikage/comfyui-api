FROM python:3.12.7-bullseye

# install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app
COPY . /app

RUN /bin/uv pip install --system --no-cache -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

EXPOSE 5000

CMD ["bash", "start.sh"]
