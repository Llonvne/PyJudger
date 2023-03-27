import subprocess
import docker


class CompileResult:
    def __init__(self, message: str):
        self.isOk = "error" not in message
        self.message = message


def compile_cpp_code_with_docker(code_str: str, source_file: str, output_file: str) -> CompileResult:
    client = docker.from_env()

    # 检查镜像是否存在
    if client.images.list(name="gpp-compiler"):
        print("检测到所需到 gpp-complier 镜像")
    else:
        print("未检测到所需到 gpp-complier 镜像，开始构建")
        dockerfile = """docker build -t gpp-compiler - <<EOF \nFROM ubuntu:latest\nRUN apt-get update && apt-get install -y g++ && rm -rf /var/lib/apt/lists/*\nEOF"""
        subprocess.run(dockerfile, shell=True, text=True, stderr=subprocess.PIPE)
        if not client.images.list(name="gpp-compiler"):
            print("构建镜像失败")
        else:
            print("构建镜像成功")

    # 将代码写入源文件
    with open(source_file, "w") as f:
        f.write(code_str)

    # 使用 Docker 编译源文件
    compile_command = f"docker run --rm -v $(pwd):/src -w /src gpp-compiler g++ {source_file} -o {output_file}"
    compile_result = subprocess.run(compile_command, shell=True, text=True, stderr=subprocess.PIPE)

    # 返回编译结果
    return CompileResult(compile_result.stderr)
