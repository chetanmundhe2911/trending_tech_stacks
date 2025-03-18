🚀 AWS SageMaker Notebook Setup with VS Code Server
This guide walks you through setting up an AWS SageMaker Notebook Instance with Git Large File Storage (LFS) and VS Code Server for an enhanced development experience.

1️⃣ Set Up Environment Variables


```
export HOME=/home/ec2-user
This sets the HOME environment variable to /home/ec2-user, which is the default home directory for an EC2/SageMaker instance user.
2️⃣ Install Git LFS (Large File Storage)
```


# Install and enable Git LFS  
```
curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.rpm.sh | sudo bash  
sudo yum install git-lfs -y  
git lfs install  
🔹 Git LFS helps manage large files in Git repositories by storing them outside the repository while keeping lightweight references inside Git.

curl fetches the installation script for Git LFS.
yum install git-lfs -y installs the package on the EC2/SageMaker instance.
git lfs install initializes Git LFS in the environment.

```


3️⃣ Clone Your Repository
```
git clone https://gitlab.com/juliensimon/huggingface-demos.git /home/ec2-user/SageMaker/huggingface-demos
```

🛠 What this does?

✅ Clones the huggingface-demos repository from GitLab into the /home/ec2-user/SageMaker/huggingface-demos directory.

4️⃣ Set Git Credential Cache for 24 Hours
```
# Set credential helper for 24 hours  
git config --global credential.helper cache  
git config --global credential.helper "cache --timeout=86400"

```
🔐 Stores Git credentials securely for 24 hours (86400 seconds) to avoid repeated authentication requests.


5️⃣ Install VS Code Server

# Install VS Code Server  

```
cd /home/ec2-user/SageMaker  
curl -LO https://github.com/aws-samples/amazon-sagemaker-codeserver/releases/download/v0.1.5/amazon-sagemaker-codeserver-0.1.5.tar.gz  
tar -xvzf amazon-sagemaker-codeserver-0.1.5.tar.gz
```

# Run installation scripts  

```
cd amazon-sagemaker-codeserver/install-scripts/notebook-instances  
chmod +x install-codeserver.sh setup-codeserver.sh  
sudo ./install-codeserver.sh  
sudo ./setup-codeserver.sh
```

⚡ What this does?

✅ Downloads and installs VS Code Server in SageMaker Notebook Instance.
✅ Extracts necessary files and sets up the environment.
✅ Grants execution permissions to setup scripts.
✅ Runs installation and setup scripts to make VS Code Server available inside Jupyter Notebook.

6️⃣ Start the Notebook Instance
```
export HOME=/home/ec2-user  
💡 Ensures the HOME environment variable is set correctly before using the notebook.
```

7️⃣ Enable Git LFS and VS Code Server on Startup

### Install and enable Git LFS  
### This must be repeated each time because the install is not persistent  
```curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.rpm.sh | sudo bash  
sudo yum install git-lfs -y  
git lfs install


# Set credential helper for 24 hours  
git config --global credential.helper cache  
git config --global credential.helper "cache --timeout=86400"  

# Enable VS Code server  
cd /home/ec2-user/SageMaker/amazon-sagemaker-codeserver/install-scripts/notebook-instances  
sudo ./setup-codeserver.sh

```
🔄 Why do this every time?

☑️ Git LFS setup is not persistent across reboots, so it must be re-installed each time the notebook starts.
☑️ VS Code Server must be re-enabled after each restart to be accessible.

🔥 SUMMARY
✅ Git LFS is installed to manage large files efficiently in Git.
✅ Cloned huggingface-demos repository into SageMaker .
✅ Git credentials are cached for 24 hours to avoid repeated login prompts.
✅ VS Code Server is installed and configured for enhanced coding inside SageMaker.
✅ Startup Commands help maintain the environment after rebooting the instance.

🚀 NEXT STEPS
✔ Access VS Code Inside SageMaker

➡ Open Jupyter Lab in SageMaker.
➡ Launch the VS Code server plugin (from JupyterLab Launcher).
➡ Start coding inside VS Code inside SageMaker!

✔ Using Git LFS for Large Models/Data

➡ Git LFS helps manage large ML models and datasets in Git repositories.
➡ Use git lfs track "*.model" to monitor large files in repositories.

