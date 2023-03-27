import subprocess

import docker

from Entities import CppRunnerRequest
from timeout import timeout


@timeout(10)
def run_cpp_native_with_docker(request: CppRunnerRequest):
    client = docker.from_env()
    # 检查镜像是否存在
    if client.images.list(name="ubuntu"):
        print("检测到所需到 ubuntu 镜像")
    else:
        print("未检测到所需到 ubuntu 镜像，开始构建")
        dockerfile = """docker build -t ubuntu - <<EOF \nFROM ubuntu:latest\nEOF"""
        subprocess.run(dockerfile, shell=True, text=True, stderr=subprocess.PIPE)
        if not client.images.list(name="gpp-compiler"):
            print("构建镜像失败")
            return
        else:
            print("构建镜像成功")

    results = []
    for testcase in request.testcases:
        compile_command = f"docker run -i --rm -v $(pwd):/src -w /src ubuntu:latest ./target/{request.submission_id}"
        program = subprocess.Popen(compile_command, shell=True, text=True, stderr=subprocess.PIPE,
                                   stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        program.stdin.write(testcase.input + "\n")
        program.stdin.flush()
        program.wait()
        results.append({
            "expect": testcase.output,
            "stdout": program.stdout.read(),
            "stderr": program.stderr.read(),
        })
    return results


if __name__ == "__main__":
    print(run_cpp_native_with_docker(1))
