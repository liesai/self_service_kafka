variable "kafka_cluster_id" {
  type = string
}

variable "topic_name" {
  type = string

  validation {
    condition     = can(regex("^[a-z0-9]+\.[a-z0-9]+\.[a-z0-9]+\.(dev|qa|prod)$", var.topic_name))
    error_message = "Topic name must follow naming convention: team.event.version.env"
  }
}

variable "partitions" {
  type = number
  validation {
    condition     = var.partitions <= 12
    error_message = "Max allowed partitions is 12."
  }
}

variable "retention_days" {
  type = number
  validation {
    condition     = var.retention_days <= 7
    error_message = "Max allowed retention is 7 days."
  }
}

variable "service_account_id" {
  type = string
}

resource "confluent_kafka_topic" "topic" {
  kafka_cluster {
    id = var.kafka_cluster_id
  }

  topic_name       = var.topic_name
  partitions_count = var.partitions

  config = {
    "retention.ms" = tostring(1000 * 60 * 60 * 24 * var.retention_days)
  }

  lifecycle {
    prevent_destroy = true
  }
}

resource "confluent_kafka_acl" "write" {
  kafka_cluster {
    id = var.kafka_cluster_id
  }

  resource_type = "TOPIC"
  resource_name = var.topic_name
  pattern_type  = "LITERAL"
  principal     = "User:${var.service_account_id}"
  operation     = "WRITE"
  permission    = "ALLOW"
}

resource "confluent_kafka_acl" "read" {
  kafka_cluster {
    id = var.kafka_cluster_id
  }

  resource_type = "TOPIC"
  resource_name = var.topic_name
  pattern_type  = "LITERAL"
  principal     = "User:${var.service_account_id}"
  operation     = "READ"
  permission    = "ALLOW"
}
