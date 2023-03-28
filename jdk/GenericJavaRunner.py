from Entities import RunnerRequest
from abstract.DockerBasedStandardRunner import DockerBasedStandardRunner


class GenericJavaRunner(DockerBasedStandardRunner):
    def __init__(self, version: int):
        super().__init__(f"jdk{version}_compiler", f"FROM openjdk:{version}")
        self.version = version

    def get_version(self) -> str:
        return str(self.version)

    def get_command(self, request: RunnerRequest):

        # 如果 Java 版本高于 11，直接使用 java xxx.java 执行
        if self.version >= 11:
            return f"java ./target/{request.submission_id}/{request.submission_id}.java"
        else:

            # # 不然首先检查是否有名称冲突，有的化，删除后重新执行
            # if os.path.exists(f"./target/olderJDK/{request.submission_id}"):
            #     shutil.rmtree(f"./target/olderJDK/{request.submission_id}")
            # os.makedirs(f"./target/olderJDK/{request.submission_id}")

            # 将 {request.submission_id}.java -> /olderJDK/{request.submission_id}/Main.java
            with open(f"./target/{request.submission_id}/{request.submission_id}.java", 'rb') as src_file, \
                    open(f"./target/{request.submission_id}/Main.java", 'wb+') as dest_file:
                dest_file.write(src_file.read())
            # 编译，执行 Java 文件
            return f"javac ./target/{request.submission_id}/Main.java;cd ./target/{request.submission_id}/;java Main"
