### CREATE NOTEBOOK INSTANCE

export HOME=/home/ec2-user

# Install and enable Git LFS
curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.rpm.sh | sudo bash
sudo yum install git-lfs -y 
git lfs install

# Clone my repository
git clone https://gitlab.com/juliensimon/huggingface-demos.git /home/ec2-user/SageMaker/huggingface-demos

# Set credential helper for 24 hours
git config --global credential.helper cache
git config --global credential.helper "cache --timeout=86400"

# Install VS Code server
cd /home/ec2-user/SageMaker
curl -LO https://github.com/aws-samples/amazon-sagemaker-codeserver/releases/download/v0.1.5/amazon-sagemaker-codeserver-0.1.5.tar.gz
tar -xvzf amazon-sagemaker-codeserver-0.1.5.tar.gz
cd amazon-sagemaker-codeserver/install-scripts/notebook-instances
chmod +x install-codeserver.sh
chmod +x setup-codeserver.sh
sudo ./install-codeserver.sh
sudo ./setup-codeserver.sh

### START NOTEBOOK INSTANCE

export HOME=/home/ec2-user

# Install and enable Git LFS
# We need to do this every time as the install is not on the persistent volume
curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.rpm.sh | sudo bash
sudo yum install git-lfs -y 
git lfs install

# Set credential helper for 24 hours
git config --global credential.helper cache
git config --global credential.helper "cache --timeout=86400"

# Enable VS Code server
cd /home/ec2-user/SageMaker
cd amazon-sagemaker-codeserver/install-scripts/notebook-instances
sudo ./setup-codeserver.sh
