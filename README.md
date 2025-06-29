---


# 🏗️ Django Project — CI/CD with TeamCity, SonarQube, AWS ECR & Auto Scaling

![image](https://github.com/user-attachments/assets/86b23f6e-417a-4b4f-8218-94d9634df8d7)



---

## 📌 Overview

This project demonstrates a **robust end-to-end pipeline** for deploying a production-grade **Django** application with:

- 🏗️ **Dockerized Django app**
- ✅ **CI/CD pipeline** powered by **TeamCity**
- 🔍 **Static code analysis** with **SonarQube**
- 🐳 **Container registry** with **AWS ECR**
- ☁️ **Highly available deployment** using:
  - **Launch Template**
  - **Auto Scaling Group (ASG)**
  - **Elastic Load Balancer (ALB)**
- 🔒 **Secure IAM roles**
- 💡 **Zero downtime rolling updates**

---

## 📁 Project Structure

```plaintext
├── django_app/           # Your Django project
├── Dockerfile            # Builds Django app image
├── docker-compose.yml    # Local dev with SonarQube, TeamCity, DB
├── .teamcity/            # TeamCity configs (optional)
├── sonar-project.properties  # SonarQube config
└── README.md             # This file
````

---

## ⚙️ Key AWS Services Used

* **EC2**: Ubuntu 22.04 instances running Docker
* **IAM**: Roles for EC2 & CI agents (least privilege)
* **ECR**: Stores built Docker images
* **Auto Scaling Group**: Ensures desired capacity & rolling deploys
* **Launch Template**: User Data script pulls & runs latest image
* **ALB (Application Load Balancer)**: Routes traffic to healthy EC2s
* **VPC/Security Groups**: Control network & ports

---

## 🚀 CI/CD Pipeline (TeamCity)

### ✅ Pipeline Steps

1️⃣ **Build**

* Build the Docker image for the Django app.

2️⃣ **Static Analysis**

* Run SonarQube scan for code quality.

3️⃣ **Push to ECR**

* Tag & push the Docker image to your AWS ECR repository.

4️⃣ **Deploy**

* Trigger an **AWS ASG Instance Refresh** to roll out new containers:

  ```bash
  aws autoscaling start-instance-refresh \
    --auto-scaling-group-name django-teamscity-asg \
    --strategy Rolling \
    --preferences MinHealthyPercentage=50,InstanceWarmup=60
  ```

---

## 📄 User Data (Launch Template)

Your EC2 instances run this on boot:

```bash
#!/bin/bash
set -ex

# Update & install dependencies
apt-get update -y
apt-get install -y docker.io unzip curl

# Start Docker
systemctl start docker
systemctl enable docker

# Add ubuntu to docker group
usermod -aG docker ubuntu

# Install AWS CLI
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
./aws/install

# Authenticate to ECR
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin 005698944845.dkr.ecr.us-east-1.amazonaws.com

# Pull latest image & run
docker pull 005698944845.dkr.ecr.us-east-1.amazonaws.com/projects/djangoteamscity:latest

docker run -d -p 80:8000 --name django-app \
  005698944845.dkr.ecr.us-east-1.amazonaws.com/projects/djangoteamscity:latest
```

---

## 🔐 IAM Setup

| Who                   | What                    |
| --------------------- | ----------------------- |
| **TeamCity IAM User** | ECR FullAccess for push |
| **EC2 Instance Role** | ECR ReadOnly for pull   |

No hardcoded credentials in instances. ✅

---

## ⚡ Quick Commands

**Build & Push manually:**

```bash
docker build -t django-teamscity:latest .
docker tag django-teamscity:latest 005698944845.dkr.ecr.us-east-1.amazonaws.com/projects/djangoteamscity:latest
docker push 005698944845.dkr.ecr.us-east-1.amazonaws.com/projects/djangoteamscity:latest
```

**Trigger ASG refresh manually:**

```bash
aws autoscaling start-instance-refresh \
  --auto-scaling-group-name django-teamscity-asg \
  --strategy Rolling \
  --preferences MinHealthyPercentage=50,InstanceWarmup=60
```

---

## 📈 SonarQube

* Runs in local Docker for scans.
* `sonar-project.properties` defines project key, server URL, auth token.

---

## 🔗 Useful URLs

| Service          | URL                               |
| ---------------- | --------------------------------- |
| **TeamCity UI**  | `http://localhost:8111`           |
| **SonarQube UI** | `http://localhost:9000`           |
| **ALB DNS**      | `http://<your-load-balancer-dns>` |

---

## 🧩 Extending This

* Add Blue/Green or Canary deployments
* Add database migrations as a pipeline step
* Automate with Terraform or CloudFormation
* Use Parameter Store or Secrets Manager for config

---

## ✅ Status

* [x] Build
* [x] Push to ECR
* [x] ASG Rolling Deploy
* [x] Load Balanced & Scalable

---



