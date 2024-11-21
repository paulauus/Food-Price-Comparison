terraform {
  required_providers {
    supabase = {
      source  = "supabase/supabase"
      version = "~> 1.0"
    }
    null = {
      source = "hashicorp/null"
      version = "~> 3.0"
    }
  }
}

provider "supabase" {
  access_token = var.API_KEY
}

resource "null_resource" "apply_schema" {
  provisioner "local-exec" {
    command = "psql -h ${var.DB_HOST} -p ${var.DB_PORT} -U ${var.DB_USER} -d ${var.DB_NAME} -f ${path.module}/../schema/schema.sql"
    environment = {
      PGPASSWORD = var.DB_PASSWORD
    }
  }
}
