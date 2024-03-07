import argparse
import json
import logging
import os
import pathlib
import sys
from datetime import datetime


logger = logging.getLogger(__name__)
if not os.path.exists("/home/svc-quantum//s3UploadLog/"):
    os.system("mkdir -p /home/svc-quantum/s3UploadLog/")
logger.setLevel(logging.DEBUG)
date = datetime.now().strftime("%Y%m%d%H%M%S")
# create file handler which logs even debug messages
fh = logging.FileHandler(
    filename=os.path.join("/home/svc-quantum/s3UploadLog/", f"s3_upload_{date}.log"), mode="a"
)
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create formatter and add it to the handlers
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)


def parse_args(argv):
    """Parse command line args
    Args:
        argv ([type]): CLI args
    Returns:
        [type]: [description]
    """
    parser = argparse.ArgumentParser(__name__)
    # json file mapping
    parser.add_argument(
        "--config",
        type=(
            lambda x: x
            if pathlib.Path(x).exists()
            else parser.error(f"{x} does not exist")
        ),
        help="REQUIRED: path to config file with key value pairs for authDir,proxy,awsPath,localSource,destinationBucket,trustAnchorArn,profileArn,roleArn",
        required=True,
        default=None,
    )
    parser.add_argument(
        "--authDir",
        type=str,
        help="OPTIONAL: dir that consists of certificate, private key, aws_signing_helper which will be used to generate aws credentials",
        required=False,
        default=None,
    )
    args = parser.parse_args(argv)
    return args


class S3Helper:
    def __init__(self, config_file_path=None) -> None:
        """constructor
        Args:
            iam_role (str, optional): IAM role ARN string. Defaults to None.
        """
        # self.config_file = config_file
        self.proxy = ""
        self.authDir = ""
        self.trustAnchorArn = ""
        self.profileArn = ""
        self.roleArn = ""
        self.awsPath = ""
        self.srcPath = ""
        self.destPath = ""
        self.logPath = ""

    def get_credentials(self, config_file_path: str) -> None:
        # config file must be in the current working directory
        config_file = os.path.basename(config_file_path)
        with open(config_file, "r") as myfile:
            arns = json.load(myfile)

        print(f"arns = [{arns}]")

        # fetch all variables from config file
        self.proxy = arns["proxy"].strip()
        self.authDir = arns["authDir"].strip()
        self.trustAnchorArn = arns["trustAnchorArn"].strip()
        self.profileArn = arns["profileArn"].strip()
        self.roleArn = arns["roleArn"].strip()
        self.awsPath = arns["awsPath"].strip()
        self.srcPath = arns["localSource"].strip()
        self.destPath = arns["destinationBucket"].strip()
        self.logPath = arns["logPath"].strip()

        os.path.exists(self.logPath)

        credentialHelper = os.path.join(self.authDir, "aws_signing_helper")
        certFile = os.path.join(
            self.authDir, os.popen("hostname").read().split(".")[0].strip() + ".cer"
        )
        privateKey = os.path.join(
            self.authDir, os.popen("hostname").read().split(".")[0].strip() + ".pem"
        )
        #set https_proxy env variable
        os.environ["https_proxy"] = str(self.proxy)

        source = self.srcPath
        destination = self.destPath

        # set execute permission for aws_signing_helper
        #os.system("chmod +x aws_signing_helper")
        logger.info(f'============ {"setting"} ============')

        #tokenFetch without proxy settings
        #tokenFetchCommand = f"{credentialHelper} credential-process --trust-anchor-arn {self.trustAnchorArn} --profile-arn {self.profileArn} --role-arn {self.roleArn} --certificate {certFile} --private-key {privateKey}"

        #Token with proxy
        tokenFetchCommand = f"export https_proxy={self.proxy}; {credentialHelper} credential-process --trust-anchor-arn {self.trustAnchorArn} --profile-arn {self.profileArn} --role-arn {self.roleArn} --certificate {certFile} --private-key {privateKey} --with-proxy"
        print(f"token fetch command = [{tokenFetchCommand}]")

        token = json.loads(os.popen(tokenFetchCommand).read())

        for k, v in token.items():
            print(k + "\n\t" + str(v))
            if k == "AccessKeyId":
                os.environ["AWS_ACCESS_KEY_ID"] = str(v)
                logger.info(
                    f" ============ setting env variable AWS_ACCESS_KEY_ID  = [{str(v)}]============"
                )
            if k == "SecretAccessKey":
                os.environ["AWS_SECRET_ACCESS_KEY"] = str(v)
                logger.info(
                    f" ============ setting env variable AWS_SECRET_ACCESS_KEY = [{str(v)}]============"
                )
            if k == "SessionToken":
                os.environ["AWS_SESSION_TOKEN"] = str(v)
                logger.info(
                    f" ============ setting env variable AWS_SESSION_TOKEN = [{str(v)}]============"
                )

        command_1 = "/usr/local/bin/aws sts get-caller-identity"
        command_2 = (
            "/usr/local/bin/aws s3 sync " + source + " " + destination
        )

        logger.info(
            f" ============ aws sts get-caller-identity [{datetime.now().time()}] ----->"
        )

        logger.info(
            f" ============ sts get-caller-identity [{os.system(command_1)}] ============"
        )
        logger.info(
            f" ============ syncing contents of [{source}] with [{destination}] ============"
        )
        logger.info(
            f' ============ {"upload in progress, please hang on..."}============'
        )

        os.system(command_2)
        logger.info(
            f" ============ syncing complete from [{source}] to [{destination}] ============"
        )


def main(argv):
    """Main function
    Args:
        argv ([type]): Command line args
    """
    args = parse_args(argv)
    s3_helper = S3Helper(args.config)

    logger.info("starting...")
    logger.info(f"args = [{argv}]")

    s3_helper.get_credentials(args.config)

    logger.info(
        "End of Logs.\t############################################################"
    )

    logging.shutdown()

    sys.exit(0)


if __name__ == "__main__":

    main(sys.argv[1:])  # Send all command line args to main
