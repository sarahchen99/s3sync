# IAMRoleAnywhere s3sync script
This python script is to used for AWS S3 IAMRoleAnywhere generate SecureKey, SecureAccessKeyID and SecureSessionToken export to global enviroment with dedicated proxy and sync to AWS S3 folder, then make logs.

Simple overview of use/purpose.

## Description

This python script is to used for AWS S3 IAMRoleAnywhere generate SecureKey, SecureAccessKeyID and SecureSessionToken export to global enviroment with dedicated proxy and sync to AWS S3 folder, then make logs.

## Getting Started

### Dependencies

* Apply certs from mfgsec, once got the keychain plus certificate upload the certificate to /home/svc-quantum/awsCerts/
   ```
   [svc-quantum@wf-p2s3-6 awsCerts]$ ls -al
      -rwxrwxrwx. 1 root        root         13400616 Feb 18 13:18 aws_signing_helper
      -rwxrwxrwx. 1 root        root             1708 Feb 17 11:39 wf-p2s3-6.cer
	  -rwxrwxrwx. 1 root        root             1704 Feb 17 11:39 wf-p2s3-6.key
	  -rwxrwxrwx. 1 root        root             1704 Feb 18 12:57 wf-p2s3-6.pem
   ```


### Installing

* download and install aws_signing_helper, awscliv2
* Any modifications needed to be made to files/folders
* prepare arn-config.json file like this format:
 # arn-config.json examples
 ```
[svc-quantum@wf-p2s3-6 ~]# cat /home/svc-quantum/s3upload/arn-config.json
{
"authDir" : "/home/svc-quantum/s3upload/awsCerts", # where certificate folder path
"retentionTime" : 7 ,
"proxy" : "http://jpa-fwdproxy-lb-1-0938db00b53b2673.elb.ap-northeast-1.amazonaws.com:3128",
"trustAnchorArn" : "arn:aws:rolesanywhere:ap-northeast-1:773566138612:trust-anchor/bfa54db4-bd37-42d2-9caa-a7d0a32b601a",
"profileArn" : "arn:aws:rolesanywhere:ap-northeast-1:773566138612:profile/f8079af3-e050-467a-bcb5-61a348d0635c",
"roleArn" : "arn:aws:iam::773566138612:role/MfgsecRoleanywhereWfP2S3UploadRole",
"awsPath" : "/usr/local/bin/aws",
"localSource" : "/mnt/hypernova/data/oc/Geortek/Celeste/Outbound/Raw/", #AWS S3 sync source folder
"destinationBucket" : "s3://mfghwteste-landing-bucket/mfghwteste-quantum_prod/Goertek/wef102/Celeste",  #AWS S3 bucket path, sync destination folder
"logPath" : "/var/log/quantum/SMT_QDF/",
"archivePath" : "/var/log/quantum/raw_archive/"
}
```
  

### Executing program

* How to manual run ? before automate, try manual test first

 ```
python s3_sync.py --config arn-config.json >> /var/log/quantum/SMT_QDF/hypernova_smt_`date +\%Y\%m\%d\%H\%M`.log

  ```

```
[svc-quantum@wf-p2s3-6 ~]# cd /home/svc-quantum/s3upload
[svc-quantum@wf-p2s3-6 s3upload]# python s3_sync.py --config arn-config.json >> /var/log/quantum/SMT_QDF/hypernova_smt_`date +\%Y\%m\%d\%H\%M`.log
2024-03-07 08:51:44,210 - __main__ - INFO - starting...
2024-03-07 08:51:44,210 - __main__ - INFO - args = [['--config', 'arn-config.json']]
2024-03-07 08:51:44,218 - __main__ - INFO - ============ setting ============
2024-03-07 08:51:44,662 - __main__ - INFO -  ============ setting env variable AWS_ACCESS_KEY_ID  = [ASIA3IHBCRD2C6Y2VS2Y]============
2024-03-07 08:51:44,662 - __main__ - INFO -  ============ setting env variable AWS_SECRET_ACCESS_KEY = [JY2P7bBU42XkrRmcwJyD8jPqWwC0MfAY40j5CyE+]============
2024-03-07 08:51:44,662 - __main__ - INFO -  ============ setting env variable AWS_SESSION_TOKEN = [IQoJb3JpZ2luX2VjEMH//////////wEaDmFwLW5vcnRoZWFzdC0xIkYwRAIgM2qXSLkJSsKeKHM39mWlc6iG41Pi6+CECzKdratc/pwCIAf0X1dmO/jTN5/T9yR0GTP1dB4YF7eu1JniW8opgrdxKtcFCLr//////////wEQBBoMNzczNTY2MTM4NjEyIgxHiiroM8T4DYITY0gqqwVWU/VfRJpMyo4D2NK2t9yaLqRwrDoM3UDO7THr0rKd32vwIn2le6s3qKAlrZNIWUJA35GoqGrs618rusEeNpr0/vByj+liciV7xD8z6Zu2DaecZTD4p/Zj/SI2CfTE/FfyVzbBONwuaxSLoFxdxBFBb2r21vMN0adAtLX6dVPAY7nif4rl7yjV4yLBcSByNwtfvx4s7NpPVgyqwnyPu2Q8tqqIUg5s+nWIsRFVIwCmLWNpKujyZo3ZiaOb0ZbRo//vljx82JNEXNjkgEdoQc8P6wd8e8CHneD7gJAF2oHczPkamGtI9hsoSR2K8Gn1XdBOTJVIlsHO5/BkiBKDbgnU3okKhhJSjefB2BbLy+7abFlUofHE6hS7kln+Z8B1Vpk87cAiROmKUUS+c0IhVv8q4X3Y3/F0EvmJ33umcoqwtuHDgluwSsbc0CEoN6nu7/lcn7O2O831RjPg+EE4q6nsweArUsd99zW9Rw5ngP5SnrSeDMCZgKJUD8jzocwrDAlNMqhDwTCubqAj0yQoFxkQ6xNGgMLMSCmMfcluLoXYgtudw5dyPcJ5OLjfUKa6D25nK8XwZb+a8FiOLTo2v39Fk+C6/vNfEdpjnsAGsr+NnRGAiEEOKdlsDD3Tt/dHJMvTxErsOgqrTUBokSTBv6FxON6mL6kql01QhRnLbFWRxWamuhsrIDOwQugry7+KGGWKm5YlwHp8El93YfG8L7a8wjXYJjK9m3TQm4TZs7evytM5Ofe54Sb9/YNsimLDkLBN98cAWC8FcB77G/MscI+yosgJxLhWox6IyQgI9AqxZeIva4K13YJ+ACE9fD38t+vl8yITcg86IqtO+gput/gxwFhCoki1IBzV7RoRGAZX/DbH8mvICtInnnf9bojK+KlpFLV983UEk3cj4TCggKavBjqUAZ0DjS6Lnt6uLR9zfjB1Etev8j4yl5VYUMxMngVQlR+K+QdHgRpr2PKv/avUntDGi/dgSzL6lFy6FzQdVNS3JOnw3W3wPXQXv/o2pGYQkvIYMir4PqMKhd45zWEE4HB58Pqc1W5Er/AOFEPMnwL80McjBHuBx6FBOiL42Be0h9b6DNoASXfNLbzvWt2nP5Z1IY+/iI4=]============
2024-03-07 08:51:44,662 - __main__ - INFO -  ============ aws sts get-caller-identity [08:51:44.662730] ----->
2024-03-07 08:51:45,690 - __main__ - INFO -  ============ sts get-caller-identity [0] ============
2024-03-07 08:51:45,690 - __main__ - INFO -  ============ syncing contents of [/mnt/hypernova/data/oc/Geortek/Celeste/Outbound/Raw/] with [s3://mfghwteste-landing-bucket/mfghwteste-quantum_prod/Goertek/wef102/Celeste] ============
2024-03-07 08:51:45,690 - __main__ - INFO -  ============ upload in progress, please hang on...============
2024-03-07 08:52:00,134 - __main__ - INFO -  ============ syncing complete from [/mnt/hypernova/data/oc/Geortek/Celeste/Outbound/Raw/] to [s3://mfghwteste-landing-bucket/mfghwteste-quantum_prod/Goertek/wef102/Celeste] ============
2024-03-07 08:52:00,134 - __main__ - INFO - End of Logs.	############################################################

```

# setup cronjobs, every 30mins sync to aws s3 and log.
```
[svc-quantum@wf-p2s3-6 ~]# crontab -l -u svc-quantum
#Push Greatwhite/project SMT/fatp/RAW/AOI data to AWS S3
*/30 * * * * source /etc/profile; flock -xn /home/svc-quantum/lockfiles/hypernova_smt.lock -c "cd /home/svc-quantum/s3upload;python s3_sync.py --config arn-config.json" >> /var/log/quantum/SMT_QDF/hypernova_smt_`date +\%Y\%m\%d\%H\%M`.log
```



## Version History

* 1.0 
    * fix dry-run issue
    * archive function still wip.
    * * Initial Release

# Manually run
python s3_sync.py --config arn-config.json >> /var/log/quantum/SMT_QDF/hypernova_smt_`date +\%Y\%m\%d\%H\%M`.log

