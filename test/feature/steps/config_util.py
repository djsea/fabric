# Copyright IBM Corp. 2016 All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


import subprocess
import os
import sys
from shutil import copyfile

def generateConfig(context, channelID, profile, ordererBlock="orderer.block"):
    # Save all the files to a specific directory for the test
    testConfigs = "configs/%s" % context.composition.projectName
    if not os.path.isdir(testConfigs):
        os.mkdir(testConfigs)

    configFile = "configtx.yaml"
    if os.path.isfile("configs/%s.yaml" % channelID):
        configFile = "%s.yaml" % channelID
    copyfile("configs/%s" % configFile, "%s/%s" %(testConfigs, configFile))

    # Default location: /opt/gopath/src/github.com/hyperledger/fabric/common/configtx/tool/configtx.yaml
    # Workaround until the -path option is added to configtxgen
    os.environ['ORDERER_CFG_PATH'] = testConfigs

    try:
        subprocess.check_call(["configtxgen", "-profile", profile,
                               #"-path", configFile,
                               "-outputCreateChannelTx", "%s/%s.tx" % (testConfigs, channelID),
                               "-outputBlock", "%s/%s" % (testConfigs, ordererBlock),
                               "-channelID", channelID])
    except:
        print("Unable to generate channel config data: {0}".format(sys.exc_info()[0]))


def generateCrypto(context, numOrgs=2, numPeersPerOrg=2, numOrderers=1):
    # Save all the files to a specific directory for the test
    testConfigs = "configs/%s" % context.composition.projectName
    if not os.path.isdir(testConfigs):
        os.mkdir(testConfigs)

    try:
        subprocess.check_call(["cryptogen",
                               "-peerOrgs", numOrgs,
                               "-ordererNodes", numOrderers,
                               "-peersPerOrg", numPeersPerOrg,
                               "-baseDir", testConfigs])
    except:
        print("Unable to generate crypto material: {0}".format(sys.exc_info()[0]))
