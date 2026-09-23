# Cloud Security Operations Platform

A practical cloud security engineering project that combines cloud infrastructure, networking, containerization, IAM, security monitoring, detection engineering, incident management, automated remediation, and CI/CD security validation.

The project is built locally first using Floci to emulate selected AWS services, with the goal of demonstrating how a cloud security operations workflow can be designed and automated without incurring AWS infrastructure costs.

> **Important:** This project distinguishes between locally emulated infrastructure and services that have been validated against real AWS behavior. The local Floci environment is not presented as a production AWS deployment.

---

## Project Objectives

This project is designed to demonstrate practical skills in:

- AWS-style cloud networking
- Infrastructure as Code with Terraform
- VPC and subnet design
- Public and private network segmentation
- Security group design
- EC2-style application infrastructure
- RDS-style database infrastructure
- Linux and Docker administration
- Node.js application deployment
- Application security logging
- Security event detection
- Brute-force detection
- Incident creation and tracking
- Automated remediation workflows
- CI/CD security validation
- Git and GitHub
- Security-focused documentation

The project intentionally starts with a small working architecture and builds toward a security operations workflow rather than attempting to implement every security product at once.

---

## Architecture

```text
                         Internet
                            |
                            v
                  +--------------------+
                  | Internet Gateway   |
                  +--------------------+
                            |
                            v
                  +--------------------+
                  | Public Route Table |
                  +--------------------+
                            |
                            v
                  +-----------------------------+
                  | Public Subnet                |
                  | 10.0.1.0/24                 |
                  |                              |
                  | Application Infrastructure  |
                  | EC2-style resource           |
                  +-----------------------------+
                            |
                            | TCP 3306
                            v
                  +-----------------------------+
                  | Private Subnet               |
                  | 10.0.2.0/24                 |
                  |                              |
                  | RDS-style MySQL database     |
                  +-----------------------------+


                      Security Operations Flow

                          Application Logs
                                 |
                                 v
                          Security Detection
                                 |
                                 v
                              Alert
                                 |
                                 v
                          Incident Manager
                                 |
                                 v
                            Remediation
                                 |
                                 v
                          Simulated Response
```

The application itself is currently run separately as a Docker container on the local Docker environment. It is not being presented as a live public application running on an AWS EC2 instance(due to Cost it might rack up).

---

## Technology Stack

### Cloud / Infrastructure

- AWS concepts
- Floci for local AWS-style service emulation
- Terraform
- VPC
- Subnets
- Internet Gateway
- Route Tables
- Security Groups
- EC2-style infrastructure
- RDS-style infrastructure

### Application

- Node.js
- Express.js
- MySQL
- mysql2
- Morgan
- Docker

### Security

- Security event logging
- JSON security events
- Authentication failure detection
- Brute-force detection
- Incident management
- Automated remediation workflow
- Source IP identification
- Simulated source IP blocking

### DevOps / CI/CD

- Git
- GitHub
- GitHub Actions
- Terraform validation
- Python syntax validation
- Docker image builds

### Operating Environment

- Ubuntu 24.04 on WSL2
- Docker
- AWS CLI
- Terraform

---

# 1. Local Environment

The project was developed in an Ubuntu 24.04 WSL2 environment.

Key tools used:

```text
Docker 29.8.1
Terraform
Git 2.43.0
AWS CLI 2.35.21
Python 3
Node.js
```

Docker and Floci are used locally so that the infrastructure can be tested without creating chargeable AWS resources.

---

# 2. Floci Local AWS Environment

Floci is used as the local AWS service emulator for this project.

The main Floci container exposes the local AWS-style API on:

```text
http://localhost:4566
```

The Floci web console is exposed locally on:

```text
http://localhost:4500
```

The project also uses the local Docker network to allow the application container to communicate with the emulated database service.

### Example local Docker network

```text
Docker bridge network
172.17.0.0/16
```

Example containers in the environment include:

```text
Floci        172.17.0.2
Floci UI     172.17.0.3
Floci EC2    172.17.0.4
Floci RDS    172.17.0.5
Node App     172.17.0.6
```

These addresses are local Docker addresses and should not be interpreted as AWS production addresses.

---

# 3. Terraform

Terraform is used to define the infrastructure as code.

The Terraform provider is configured for local Floci endpoints and uses test credentials because the project is running locally.

Example provider configuration:

```hcl
terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
    }
  }

  required_version = ">= 1.6.0"
}

provider "aws" {
  region                      = "us-east-1"
  access_key                  = "test"
  secret_key                  = "test"

  skip_credentials_validation = true
  skip_requesting_account_id  = true
  skip_metadata_api_check     = true

  endpoints {
    ec2 = "http://localhost:4566"
  }
}
```

Terraform is used to define:

- VPC
- Public subnet
- Private subnet
- Internet Gateway
- Public route table
- Route table association
- Application security group
- Database security group
- EC2-style application resource
- RDS-style database
- RDS subnet group

---

# 4. VPC and Network Design

The project uses the following VPC:

```text
VPC CIDR: 10.0.0.0/16
```

DNS support and DNS hostnames are enabled.

## Public subnet

```text
CIDR: 10.0.1.0/24
Availability Zone: us-east-1a
```

This subnet represents the application-facing network tier.

## Private subnet

```text
CIDR: 10.0.2.0/24
Availability Zone: us-east-1a
```

This subnet represents the database tier.

The private subnet does not have a direct Internet Gateway route.

---

# 5. Internet Gateway and Routing

An Internet Gateway is attached to the VPC.

The public route table contains:

```text
0.0.0.0/0 -> Internet Gateway
```

The public subnet is associated with this route table.

This represents the intended public network path for the application tier.

---

# 6. Security Groups

Two security groups were created.

## Application Security Group

The application security group allows:

```text
TCP 80
TCP 443
```

from:

```text
0.0.0.0/0
```

These rules represent HTTP and HTTPS access to the application layer.

## Database Security Group

The database security group allows:

```text
TCP 3306
```

from the application security group.

This models the intended principle:

```text
Internet
   |
   v
Application
   |
   v
Database
```

rather than exposing the database directly to the Internet.

---

# 7. EC2-Style Application Infrastructure

Terraform defines an EC2-style application resource with:

```text
AMI: ami-ubuntu2404-amd64
Instance type: t3.micro
Subnet: Public subnet
```

The resource is tagged as:

```text
cloud-security-app-server
```

The local Floci environment successfully created the resource.

The returned local values included:

```text
Instance ID: i-d38469f88401dc7ef
Private IP: 10.0.1.10
```

Because this is a local Floci environment, the returned public networking behavior does not represent a real public AWS EC2 instance.

A Floci limitation around modifying the network interface security group required Terraform lifecycle handling so that the local state could remain stable.

This limitation is documented rather than hidden.

---

# 8. RDS-Style Database

A MySQL database resource was created using Terraform.

Configuration includes:

```text
Engine: MySQL
Engine version: 8.0
Instance class: db.t3.micro
Storage: 20 GB
Database name: cloudsecurity
Publicly accessible: false
```

The database is associated with:

```text
Private subnet
Database security group
```

The local Floci environment returned:

```text
Database identifier:
cloud-security-database

Engine:
mysql

Port:
7001

Status:
available
```

The local endpoint returned by Floci is not equivalent to a production AWS RDS endpoint.

---

# 9. Database Connectivity Testing

The application container was used to test network connectivity to the local database service.

A TCP connectivity test confirmed that the database port was reachable.

Example:

```bash
docker exec cloud-security-platform-app \
  sh -c 'nc -zv 172.17.0.2 7001'
```

The connection succeeded.

An HTTP request against the MySQL port produced a MySQL protocol response rather than an HTTP response.

This confirmed that the service was speaking the database protocol rather than HTTP.

This was an important troubleshooting exercise because a successful TCP connection does not mean that the application protocol is HTTP.

---

# 10. Node.js Application

The application is a small Node.js service created for the security platform.

Main technologies:

```text
Node.js
Express
MySQL2
Morgan
```

The application provides:

```text
GET /
GET /health
```

## Root endpoint

The root endpoint returns information such as:

```json
{
  "application": "Cloud Security Operations Platform",
  "status": "running",
  "environment": "development"
}
```

## Health endpoint

The `/health` endpoint checks the database connection.

A successful response indicates:

```json
{
  "status": "healthy",
  "database": "connected"
}
```

If the database connection fails, the application returns an HTTP 503 response and writes a structured security event to the application logs.

---

# 11. Application Security Logging

The application generates structured JSON security events.

A helper function is used to create security events containing information such as:

```text
timestamp
event
source IP
username
error details
```

Example event type:

```text
database_connection_failed
```

This creates a useful boundary between normal application logs and security events that can later be consumed by a detection pipeline.

---

# 12. Authentication Failure Detection

The security detection component is located at:

```text
security/detections/detect.py
```

The detector reads JSON log events from standard input.

It currently detects:

### Database connection failure

```text
Alert: DATABASE_CONNECTION_FAILURE
Severity: HIGH
```

### Failed authentication

```text
Alert: FAILED_AUTHENTICATION
Severity: MEDIUM
```

### Brute-force activity

If five or more authentication failures are observed from the same source IP:

```text
Alert: BRUTE_FORCE_DETECTED
Severity: HIGH
```

The detector keeps a counter per source IP.

Example:

```text
192.168.1.50 -> 1 failed attempt
192.168.1.50 -> 2 failed attempts
192.168.1.50 -> 3 failed attempts
192.168.1.50 -> 4 failed attempts
192.168.1.50 -> 5 failed attempts
```

The fifth attempt triggers the brute-force detection.

---

# 13. Detection Pipeline

The security detection process follows:

```text
Application Log
      |
      v
JSON Event
      |
      v
detect.py
      |
      +---- Normal event -> ignored
      |
      +---- Failed authentication -> MEDIUM alert
      |
      +---- 5+ failures -> HIGH brute-force alert
```

The detector was tested with five authentication failures from the same source IP.

The expected behavior was observed:

```text
Attempts 1-4:
FAILED_AUTHENTICATION / MEDIUM

Attempt 5:
BRUTE_FORCE_DETECTED / HIGH
```

---

# 14. Incident Management

Detected alerts are passed to:

```text
security/incidents/incident_manager.py
```

The incident manager converts alerts into persistent incident records.

Incidents are stored in:

```text
security/incidents/incidents.jsonl
```

Each incident contains fields such as:

```text
incident_id
alert
severity
status
timestamp
source_ip
description
response
```

Example structure:

```json
{
  "incident_id": "INC-0001",
  "alert": "BRUTE_FORCE_DETECTED",
  "severity": "HIGH",
  "status": "OPEN",
  "source_ip": "192.168.1.50",
  "response": {
    "action": "PENDING",
    "timestamp": null
  }
}
```

The incident manager therefore creates a persistent record that can be used by later response and reporting components.

---

# 15. End-to-End Detection and Incident Test

The detection and incident pipeline was tested using five simulated authentication failures.

Example:

```bash
for i in {1..5}; do
  echo "{\"timestamp\":\"2026-09-22T21:00:0${i}Z\",\"event\":\"authentication_failed\",\"username\":\"admin\",\"source_ip\":\"192.168.1.50\"}"
done | \
python3 security/detections/detect.py | \
python3 security/incidents/incident_manager.py
```

This produced incident records including a high-severity brute-force incident.

The resulting incidents were persisted to:

```text
security/incidents/incidents.jsonl
```

---

# 16. Automated Remediation

The remediation component is located at:

```text
security/remediation/remediate.py
```

The remediation workflow checks the incident type.

For:

```text
BRUTE_FORCE_DETECTED
```

the current response is:

```text
BLOCK_SOURCE_IP
```

However, because the project is running in a local Floci environment, this action is intentionally simulated.

The remediation output contains:

```text
action: BLOCK_SOURCE_IP
status: SIMULATED
source_ip: detected source IP
```

Example:

```json
{
  "action": "BLOCK_SOURCE_IP",
  "status": "SIMULATED"
}
```

This does **not** actually block traffic.

The purpose is to demonstrate the logic and workflow that could later be connected to a real AWS security control such as a network control, firewall mechanism, WAF rule, or automated security response.

---

# 17. Remediation Testing

The remediation process was tested against the latest generated incident.

Example:

```bash
tail -n 1 security/incidents/incidents.jsonl | \
python3 security/remediation/remediate.py
```

The result produced:

```text
BLOCK_SOURCE_IP
SIMULATED
```

This confirmed that the high-severity brute-force incident could move through the incident-response pipeline.

---

# 18. Security Operations Flow

The current security workflow is:

```text
Application
    |
    v
Security Event
    |
    v
Detection Engine
    |
    v
Alert
    |
    v
Incident Manager
    |
    v
Incident Record
    |
    v
Remediation Engine
    |
    v
Simulated Security Action
```

This provides the foundation for a larger cloud security operations platform.

---

# 19. Docker

The Node.js application is containerized.

The application Docker image is:

```text
cloud-security-platform-app
```

The application container exposes:

```text
3000
```

Example local run:

```bash
docker run -d \
  --name cloud-security-platform-app \
  --env-file application/.env \
  -p 3000:3000 \
  cloud-security-platform-app:1.3
```

The environment file contains sensitive database configuration and is excluded from Git.

The `.gitignore` file includes:

```text
.env
*.env
application/node_modules/
terraform/.terraform/
terraform/*.tfstate
terraform/*.tfstate.*
terraform/*.tfvars
```

Credentials and local Terraform state are therefore not intended to be committed to the repository.

---

# 20. GitHub Repository

Repository:

```text
https://github.com/AyomideADEJARE1/cloud-security-operations-platform
```

The repository contains the infrastructure, application, detection, incident, remediation, and CI/CD components.

Main structure:

```text
cloud-security-operations-platform/
│
├── terraform/
│   ├── main.tf
│   ├── providers.tf
│   ├── variables.tf
│   ├── outputs.tf
│   ├── vpc.tf
│   ├── subnets.tf
│   ├── internet.tf
│   ├── security-groups.tf
│   ├── ec2.tf
│   ├── rds.tf
│   └── iam.tf / monitoring.tf
│
├── application/
│   ├── app.js
│   ├── package.json
│   ├── package-lock.json
│   ├── Dockerfile
│   └── .dockerignore
│
├── security/
│   ├── detections/
│   │   └── detect.py
│   ├── incidents/
│   │   ├── incident_manager.py
│   │   ├── incident.json
│   │   └── incidents.jsonl
│   └── remediation/
│       ├── remediate.py
│       └── remediation.jsonl
│
├── docs/
├── screenshots/
├── .github/
│   └── workflows/
│       └── security-pipeline.yml
│
├── .gitignore
└── README.md
```

Some infrastructure files such as IAM and monitoring are planned for later phases and may not yet be present in the current implementation.

---

# 21. GitHub Actions CI/CD Security Validation

The repository contains:

```text
.github/workflows/security-pipeline.yml
```

Workflow name:

```text
Cloud Security Platform CI
```

The workflow runs on pushes and pull requests targeting:

```text
master
```

The pipeline currently performs:

1. Repository checkout
2. Terraform setup
3. Terraform formatting check
4. Terraform initialization
5. Terraform validation
6. Python setup
7. Python syntax checks
8. Docker image build

---

# 22. Terraform CI Validation

The workflow runs:

```bash
terraform fmt -check -recursive
```

and:

```bash
terraform init -backend=false
```

followed by:

```bash
terraform validate
```

This ensures that Terraform configuration remains correctly formatted and syntactically valid.

---

# 23. Python CI Validation

The security components are checked using Python's bytecode compilation:

```bash
python -m py_compile security/detections/detect.py
python -m py_compile security/incidents/incident_manager.py
python -m py_compile security/remediation/remediate.py
```

This catches Python syntax errors before changes are accepted into the project.

---

# 24. Docker CI Validation

The CI pipeline builds the application image:

```bash
docker build -t cloud-security-platform-app:ci .
```

This verifies that the application Dockerfile remains buildable.

---

# 25. CI Pipeline Result

The CI workflow was successfully pushed to GitHub after the repository's Personal Access Token was updated with the permission required to create or update GitHub Actions workflow files.

The GitHub Actions workflow subsequently completed successfully.

This demonstrates a basic DevSecOps feedback loop:

```text
Developer
   |
   v
Git push / Pull Request
   |
   v
GitHub Actions
   |
   +--> Terraform validation
   |
   +--> Python validation
   |
   +--> Docker build
   |
   v
Validation result
```

---

# 26. Security Design Principles Demonstrated

The project demonstrates several practical security principles.

## Network segmentation

The application and database are separated into different subnets.

```text
Public subnet
    |
    v
Application
    |
    v
Private subnet
    |
    v
Database
```

## Least exposure

The database is intended to be private and only reachable by the application tier.

## Structured logging

Security events are represented as structured JSON instead of relying only on human-readable log text.

## Detection thresholds

Repeated authentication failures are correlated by source IP to identify potential brute-force activity.

## Incident persistence

Alerts are converted into persistent incident records.

## Automated response

Detected incidents can trigger a defined response workflow.

## Safe automation

The current response is simulated locally instead of making potentially destructive changes to a real cloud environment.

## Infrastructure as Code

Infrastructure is defined using Terraform rather than being created only through a graphical interface.

## Continuous validation

GitHub Actions automatically validates infrastructure, Python security code, and the application container build.

---

# 27. Troubleshooting Experience

The project also involved practical troubleshooting rather than only successful configuration.

### Floci UI runtime socket issue

The Floci web console initially reported:

```text
Floci could not reach the container runtime
java.net.SocketException: No such file or directory
```

This was related to container runtime socket access from the Floci UI.

The runtime/socket configuration was corrected and the Floci UI became available.

This demonstrated the importance of checking:

- Docker socket availability
- Container volume mounts
- Runtime permissions
- Container-to-host communication

### Kubernetes / container environment experience

The project environment also involved working with Docker, WSL2, and local container tooling, including troubleshooting stopped local Kubernetes clusters and container networking.

These exercises helped build practical Linux and container administration experience alongside the main project.

---

# 28. Local Validation Commands

### Terraform

```bash
cd terraform

terraform fmt -check -recursive
terraform validate
```

### Python

```bash
python3 -m py_compile security/detections/detect.py
python3 -m py_compile security/incidents/incident_manager.py
python3 -m py_compile security/remediation/remediate.py
```

### Docker

```bash
docker build -t cloud-security-platform-app:ci application/
```

### Application health check

```bash
curl http://localhost:3000/health
```

Expected successful response:

```json
{
  "status": "healthy",
  "database": "connected"
}
```

---

# 29. Current Project Status

The following components are currently implemented and tested:

- [x] Local Floci environment
- [x] Terraform provider configuration
- [x] VPC
- [x] Public subnet
- [x] Private subnet
- [x] Internet Gateway
- [x] Public route table
- [x] Route table association
- [x] Application security group
- [x] Database security group
- [x] EC2-style infrastructure
- [x] RDS-style MySQL database
- [x] Node.js application
- [x] Dockerized application
- [x] Application health endpoint
- [x] Structured security logging
- [x] Authentication failure detection
- [x] Brute-force detection
- [x] Incident management
- [x] Incident persistence
- [x] Simulated automated remediation
- [x] GitHub repository
- [x] GitHub Actions CI validation
- [x] Terraform validation
- [x] Python syntax validation
- [x] Docker image validation

---

# 30. Planned Next Stages

The platform is intended to grow into a broader cloud security operations project.

Potential next stages include:

### IAM

- IAM users and roles
- Least-privilege policies
- Role-based access
- Instance roles
- Security policy validation

### Monitoring

- Cloud-style audit logging
- Centralized security logs
- Security event correlation
- Monitoring dashboards

### Detection Engineering

Additional detections could include:

- Suspicious privilege escalation
- Unexpected security group changes
- Unusual network activity
- Unauthorized IAM changes
- Suspicious API activity

### Incident Response

Future improvements could include:

- Incident severity handling
- Incident state transitions
- Response playbooks
- Evidence collection
- Incident timelines

### Automated Remediation

The simulated remediation layer could eventually be connected to real AWS controls.

For example:

```text
Detection
    |
    v
Incident
    |
    v
Automated decision
    |
    v
AWS security control
```

Any real AWS remediation would be tested carefully because automated security actions can affect production resources.

### DevSecOps

Future CI/CD improvements may include:

- Terraform security scanning
- Dependency scanning
- Container vulnerability scanning
- Secret scanning
- Static application security testing
- Policy-as-code
- Deployment gates

---

# 31. Local vs Real AWS

This distinction is important to the project.

## Implemented locally

The following are primarily tested through Floci/local Docker:

- VPC-style infrastructure
- Subnets
- Internet Gateway
- Route tables
- Security groups
- EC2-style resources
- RDS-style resources
- Application container
- Security detection
- Incident management
- Remediation workflow

## Validated through tooling

The project also uses:

- Terraform
- AWS CLI
- Docker
- GitHub Actions

to validate configuration and workflow behavior.

## Not claimed as production AWS

The project does not claim that the local Floci environment is equivalent to a production AWS environment.

Some AWS APIs and networking behaviors are not fully implemented by local emulation.

Where a Floci limitation was encountered, Terraform lifecycle handling or documentation was used rather than pretending that the local behavior was identical to AWS.

---

# 32. Security and Credential Handling

No real AWS credentials are required for the local Floci environment.

The Terraform provider uses test credentials for the local emulator.

Application database credentials are stored in a local environment file and are excluded from Git.

Sensitive values should never be committed to the repository.

Before using the project with real AWS resources, credentials should be supplied through an appropriate AWS authentication mechanism such as:

- AWS CLI configuration
- Environment variables
- IAM roles
- GitHub Actions OIDC
- AWS Secrets Manager

depending on the deployment environment.

---

# 33. What This Project Demonstrates

This project demonstrates the ability to connect multiple areas of IT and security engineering into one workflow:

```text
Networking
    +
Cloud Infrastructure
    +
Linux
    +
Docker
    +
Application
    +
Security Logging
    +
Detection Engineering
    +
Incident Response
    +
Automation
    +
CI/CD
```

Instead of treating these as isolated technologies, the project connects them into an operational security workflow.

---

# 34. Skills Demonstrated

### Cloud

- AWS architecture concepts
- VPC
- Subnets
- Internet Gateway
- Route tables
- Security groups
- EC2
- RDS
- AWS CLI
- Cloud infrastructure troubleshooting

### Infrastructure as Code

- Terraform
- Resource dependencies
- Terraform state
- Terraform validation
- Infrastructure lifecycle management

### Networking

- IPv4 addressing
- CIDR
- Public/private subnet design
- Routing
- TCP connectivity
- Port-based access control
- Network segmentation
- Security group concepts

### Linux

- Ubuntu
- WSL2
- Shell commands
- Process and service troubleshooting
- File and directory management
- Container networking

### Containers

- Docker
- Dockerfiles
- Docker images
- Docker containers
- Environment variables
- Container networking
- Application containerization

### Security

- Security logging
- Event detection
- Authentication monitoring
- Brute-force detection
- Incident management
- Automated remediation concepts
- Least privilege
- Network segmentation

### DevSecOps

- Git
- GitHub
- GitHub Actions
- Infrastructure validation
- Application validation
- Container build validation

### Programming / Automation

- Python
- JavaScript
- JSON
- Bash
- Node.js
- Express

---

# 35. Project Outcome

The project currently provides a working foundation for a cloud security operations platform.

The infrastructure is defined as code, the application is containerized, security events are generated and detected, alerts can become incidents, and incidents can trigger simulated remediation.

The CI pipeline then validates the infrastructure and application components automatically.

The architecture is intentionally designed so that future components can be added without rebuilding the entire project from scratch.

---

## Author

**Ayomide Adejare**

GitHub:

```text
https://github.com/AyomideADEJARE1
```

Project:

```text
https://github.com/AyomideADEJARE1/cloud-security-operations-platform
```
