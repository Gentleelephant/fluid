# 使用 Ubuntu 22.04 作为基础镜像
FROM ubuntu:22.04

# 更新包列表并安装必要的工具
RUN apt-get update && \
    apt-get install -y \
    python3 \
    bash \
    nfs-common \
    && rm -rf /var/lib/apt/lists/*

# 添加 Python 脚本和入口脚本
ADD fluid_config_init.py /
ADD entrypoint.sh /usr/local/bin/

# 设置入口脚本的执行权限
RUN chmod +x /usr/local/bin/entrypoint.sh

# 设置容器启动时执行的命令
CMD ["/usr/local/bin/entrypoint.sh"]