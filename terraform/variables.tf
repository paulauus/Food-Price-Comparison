variable "API_URL" {
  description = "Supabase API URL"
  type        = string
}

variable "API_KEY" {
  description = "Supabase API Key"
  type        = string
}

variable "DB_NAME" {
  description = "Supabase Database Name"
  type        = string
}

variable "DB_HOST" {
  description = "Supabase Database Host"
  type        = string
}

variable "DB_PORT" {
  description = "Supabase Database Port"
  type        = string
}

variable "DB_USER" {
  description = "Supabase Database User"
  type        = string
}

variable "DB_PASSWORD" {
  description = "Supabase Database Password"
  type        = string
  sensitive   = true
}
