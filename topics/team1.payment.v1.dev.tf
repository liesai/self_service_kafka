module "team1_payment_topic" {
  source              = "../modules/kafka_topic"
  kafka_cluster_id    = var.kafka_cluster_id
  topic_name          = "team1.payment.v1.dev"
  partitions          = 6
  retention_days      = 7
  service_account_id  = "sa-team1-id"
}
