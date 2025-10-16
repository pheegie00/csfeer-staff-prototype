# PostgreSQL User and Role Permissions

### Base Roles

# | Role Name | Object Type | Privileges |
# |-----------|-------------|------------|
# | db_migration | table | SELECT, INSERT, UPDATE, DELETE, TRUNCATE, REFERENCES, TRIGGER |
# | db_migration | sequence | USAGE, SELECT, UPDATE |
# | db_migration | schema | CREATE, USAGE |
# | db_admin | database | CREATE, CONNECT, TEMPORARY |
# | db_connect | database | CONNECT |
# | db_read_only | schema | USAGE |
# | db_read_only | table | SELECT |
# | db_read_only | sequence | USAGE, SELECT |
# | db_read_write | table | SELECT, INSERT, UPDATE, DELETE |

### Users and Their Roles

# | User | Roles | Inherited Permissions |
# |------|-------|----------------------|
# | csfeer_app_user | db_read_write, rds_iam, db_connect, db_read_only | SELECT, INSERT, UPDATE, DELETE on tables, AWS IAM authentication, CONNECT to database, SELECT on tables |
# | csfeer_reader_user | rds_iam, db_connect, db_read_only | AWS IAM authentication, CONNECT to database, SELECT on tables |
# | csfeer_admin_user | db_admin, rds_iam, db_connect, db_read_only | CREATE, CONNECT, TEMPORARY on database, AWS IAM authentication, CONNECT to database, SELECT on tables |
# | csfeer_migration_user | db_migration, rds_iam, db_connect, db_read_only | Table/sequence/schema permissions, AWS IAM authentication, CONNECT to database, SELECT on tables |



locals {
  databases = {
    csfeer = {
      name   = "csfeer"
      schema = local.schema_name
    }
  }
  roles = {
    db_migration = {
      name = "db_migration"
      permissions = {
        table = {
          object_type = "table"
          privileges  = ["SELECT", "INSERT", "UPDATE", "DELETE", "TRUNCATE", "REFERENCES", "TRIGGER"]
        },
        sequence = {
          object_type = "sequence"
          privileges  = ["USAGE", "SELECT", "UPDATE"]
        },
        schema = {
          object_type = "schema"
          privileges  = ["CREATE", "USAGE"]
        }
      }
    }
    db_admin = {
      name = "db_admin"
      permissions = {
        database = {
          object_type = "database"
          privileges  = ["CREATE", "CONNECT", "TEMPORARY"]
        }
      }
    }
    db_connect = {
      name = "db_connect"
      permissions = {
        database = {
          object_type = "database"
          privileges  = ["CONNECT"]
        }
      }
    }
    db_read_only = {
      name = "db_read_only"
      permissions = {
        schema = {
          object_type = "schema"
          privileges  = ["USAGE"]
        }
        table = {
          object_type = "table"
          privileges  = ["SELECT"]
        }
        sequence = {
          object_type = "sequence"
          privileges  = ["USAGE", "SELECT"]
        }
      }
    }
    db_read_write = {
      name = "db_read_write"
      permissions = {
        table = {
          object_type = "table"
          privileges  = ["SELECT", "INSERT", "UPDATE", "DELETE"]
        }
        schema = {
          object_type = "schema"
          privileges  = ["USAGE"]
        }
        sequence = {
          object_type = "sequence"
          privileges  = ["USAGE", "SELECT", "UPDATE"]
        }
      }
    }
  }

  users = {
    app = {
      name  = "app_user"
      login = true
      roles = ["db_read_write", "rds_iam", "db_connect", "db_read_only"]
    }
    reader_user = {
      name  = "reader_user"
      login = true
      roles = ["rds_iam", "db_connect", "db_read_only"]
    }
    admin_user = {
      name  = "admin_user"
      login = true
      roles = ["db_admin", "rds_iam", "db_connect", "db_read_only"]
    }
    migration_user = {
      name  = "migration_user"
      login = true
      roles = ["db_migration", "rds_iam", "db_connect", "db_read_only"]
    }
  }

  users_with_db_prefix = {
    for pair in flatten([
      for db_name, db in local.databases : [
        for user_name, user in local.users : {
          key   = "${db_name}_${user_name}"
          name  = "${db_name}_${user.name}"
          login = user.login
          roles = [for role in user.roles : role]
        }
      ]
      ]) : pair.key => {
      name  = pair.name
      login = pair.login
      roles = pair.roles
    }
  }


}

data "aws_secretsmanager_secret_version" "master_db_password" {
  secret_id = module.csfeer_rds_aurora.master_password_secret_arn[0].secret_arn
}


# Provider configuration for csfeer
provider "postgresql" {
  alias           = "csfeer"
  host            = module.csfeer_rds_aurora.endpoint
  port            = 5432
  username        = module.csfeer_rds_aurora.master_username
  password        = jsondecode(data.aws_secretsmanager_secret_version.master_db_password.secret_string)["password"]
  superuser       = false
  sslmode         = "require"
  connect_timeout = 15
}

# Create database (csfeer)
resource "postgresql_database" "csfeer_db" {
  provider               = postgresql.csfeer
  name                   = "csfeer"
  owner                  = module.csfeer_rds_aurora.master_username
  allow_connections      = true
  alter_object_ownership = true
}


# Create roles - common to both databases
resource "postgresql_role" "roles" {
  for_each = local.roles
  provider = postgresql.csfeer
  name     = each.value.name
  login    = false
}

# Create users - common to both databases
resource "postgresql_role" "users" {
  for_each = local.users_with_db_prefix
  provider = postgresql.csfeer
  name     = each.value.name
  login    = each.value.login
  roles = concat(
    [for role in each.value.roles : postgresql_role.roles[role].name if contains(keys(local.roles), role)],
    [for role in each.value.roles : role if !contains(keys(local.roles), role)]
  )
}

# Grant default privileges for future tables to db_read_write role - csfeer
resource "postgresql_default_privileges" "csfeer_db_read_write_future_tables" {
  provider    = postgresql.csfeer
  database    = local.databases.csfeer.name
  schema      = local.schema_name
  role        = local.roles.db_read_write.name
  owner       = local.users_with_db_prefix["csfeer_migration_user"].name
  object_type = "table"
  privileges  = ["SELECT", "INSERT", "UPDATE", "DELETE"]
}

resource "postgresql_default_privileges" "csfeer_db_read_write_future_sequences" {
  provider    = postgresql.csfeer
  database    = local.databases.csfeer.name
  schema      = local.schema_name
  role        = local.roles.db_read_write.name
  owner       = local.users_with_db_prefix["csfeer_migration_user"].name
  object_type = "sequence"
  privileges  = ["USAGE", "SELECT", "UPDATE"]
}

