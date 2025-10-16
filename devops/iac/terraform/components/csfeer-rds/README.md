# csfeer Database Architecture Documentation

## Overview

This document outlines the database architecture for csfeer 3.0, built on Amazon Aurora PostgreSQL. It provides details on our infrastructure, design choices, security measures, and operational configurations.

## Table of Contents

1. [Database Platform](#1-database-platform)
2. [Infrastructure](#2-infrastructure)
3. [High Availability and Scalability](#3-high-availability-and-scalability)
4. [Security and Access Control](#4-security-and-access-control)
5. [Connectivity](#5-connectivity)
6. [Data Resilience](#6-data-resilience)
7. [Monitoring and Maintenance](#7-monitoring-and-maintenance)
8. [Performance Optimization](#8-performance-optimization)

## 1. Database Platform

- **Service:** Amazon Aurora PostgreSQL
- **Description:** A distributed, high-performance relational database service

### Key Features

- Automatic data replication across 3 Availability Zones
- Auto-growing storage up to 128 TiB
- Support for up to 15 low-latency read replicas

## 2. Infrastructure

### csfeer Configuration

- **Instance Type:** db.r5.2xlarge
  - vCPUs: 8
  - RAM: 64 GiB
  - Network Performance: Up to 10 Gbps
- **Multi-AZ Deployment:** Enabled

## 3. High Availability and Scalability

### Cluster Configuration

- **Primary Instance:** 1 (handles read/write operations)
- **Read Replicas:** 2 (handles read operations, provides failover targets)

### Failover Mechanism

- Automatic failover to replica in case of primary failure
- Typical failover time: < 60 seconds

## 4. Security and Access Control

### Encryption

- Network traffic to and from the database is encrypted using Secure Socket Layer (SSL) or Transport Layer Security (TLS).
- **In-Transit:** SSL/TLS enforced (rds.force_ssl = 1)
- **Certificate:** rds-ca-rsa2048-g1 (RSA 2048-bit, SHA256)

### Authentication

- You can use IAM to centrally manage access to your database resources, instead of managing access individually on each DB cluster.
- csfeer is using AWS Identity and Access Management (IAM) database authentication. This feature allows you to authenticate to your Aurora PostgreSQL database using IAM credentials instead of a password.
- IAM database authentication enabled

### Access Control

- For applications running on Amazon EC2, you can use profile credentials specific to your EC2 instance to access your database instead of a password, for greater security.
- Users must have appropriate IAM permissions to generate auth tokens
- To connect using IAM authentication, generate a token using the AWS CLI or SDK, then use this token in place of a password when connecting to the database.
- For csfeer we have an application specific user `csfeer_app_user` which is what the Kubenetes container will use to connect to the DB. There is an IAM policy with the `rds:dbconnect` permission attached to the csfeer IAM Container Role. There are other users/roles which have been created and are shown below.

#### Base Roles

| Role Name     | Object Type | Privileges                                                    |
| ------------- | ----------- | ------------------------------------------------------------- |
| db_migration  | table       | SELECT, INSERT, UPDATE, DELETE, TRUNCATE, REFERENCES, TRIGGER |
| db_migration  | sequence    | USAGE, SELECT, UPDATE                                         |
| db_migration  | schema      | CREATE, USAGE                                                 |
| db_admin      | database    | CREATE, CONNECT, TEMPORARY                                    |
| db_connect    | database    | CONNECT                                                       |
| db_read_only  | schema      | USAGE                                                         |
| db_read_only  | table       | SELECT                                                        |
| db_read_only  | sequence    | USAGE, SELECT                                                 |
| db_read_write | table       | SELECT, INSERT, UPDATE, DELETE                                |

#### Users and Their Roles

| User               | Roles                                            | Inherited Permissions                                                                                   |
| ------------------ | ------------------------------------------------ | ------------------------------------------------------------------------------------------------------- |
| csfeer_app_user       | db_read_write, rds_iam, db_connect, db_read_only | SELECT, INSERT, UPDATE, DELETE on tables, AWS IAM authentication, CONNECT to database, SELECT on tables |
| csfeer_reader_user    | rds_iam, db_connect, db_read_only                | AWS IAM authentication, CONNECT to database, SELECT on tables                                           |
| csfeer_admin_user     | db_admin, rds_iam, db_connect, db_read_only      | CREATE, CONNECT, TEMPORARY on database, AWS IAM authentication, CONNECT to database, SELECT on tables   |
| csfeer_migration_user | db_migration, rds_iam, db_connect, db_read_only  | Table/sequence/schema permissions, AWS IAM authentication, CONNECT to database, SELECT on tables        |

## 5. Connectivity

### Endpoints

- **Primary Operations:** Cluster Endpoint
- **Read Operations:** Reader Endpoint (load-balanced)

### Network Access

- **Public Access:** Disabled
- **VPC Access:** Enabled

## 6. Data Resilience

### Backup Configuration

- **Automated Backups:** Enabled
- **Backup Retention Period:** 14 days
- **Backup Window:** 02:00-03:00 UTC

### Recovery Options

- Point-in-Time Recovery: Enabled (within retention period)
- Cross-Region Disaster Recovery: Configured via Global Database feature

## 7. Monitoring and Maintenance

### Active Monitoring

- **Performance Insights:** Enabled
- **Enhanced Monitoring:** Enabled (15-second intervals)

### Integration

- Amazon CloudWatch for metrics and alarms

## 8. Performance Optimization

- Automated recommendations for cluster optimization enabled
- Regular review of Performance Insights data
- Periodic evaluation of instance sizing and replica count
