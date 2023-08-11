from dataclasses import dataclass,field
from typing import List, Tuple


# dependency jars to read data from kafka, and connect to postgres
REQUIRED_JARS = [
    "file:///opt/flink/flink-sql-connector-kafka-1.17.0.jar",
    "file:///opt/flink/flink-connector-jdbc-3.0.0-1.16.jar",
    "file:///opt/flink/postgresql-42.6.0.jar",
]


@dataclass(frozen=True)
class StreamJobConfig:
    job_name: str = 'checkout-attribution-job'
    jars: List[str] = field(default_factory=lambda: REQUIRED_JARS)
    checkpoint_interval: int = 10
    checkpoint_pause: int = 5
    checkpoint_timeout: int = 5
    parallelism: int = 2


@dataclass(frozen=True)
class KafkaConfig:
    connector: str = 'kafka'
    bootstrap_servers: str = 'kafka:9092'
    scan_stratup_mode: str = 'earliest-offset'
    consumer_group_id: str = 'flink-consumer-group-1'


@dataclass(frozen=True)
class ClickTopicConfig(KafkaConfig):
    topic: str = 'clicks'
    format: str = 'json'

@dataclass(frozen=True)
class CheckoutTopicConfig(KafkaConfig):
    topic: str = 'checkouts'
    format: str = 'json'



@dataclass(frozen=True)
class ApplicationDatabaseConfig:
    connector: str = 'jdbc'
    url: str = 'jdbc:postgresql://postgres:5432/postgres'
    username: str = 'postgres'
    password: str = 'postgres'
    driver: str = 'org.postgresql.Driver'


@dataclass(frozen=True)
class ApplicationUsersTableConfig(ApplicationDatabaseConfig):
    table_name: str = 'commerce.users'


@dataclass(frozen=True)
class ApplicationAttributedCheckoutsTableConfig(ApplicationDatabaseConfig):
    table_name: str = 'commerce.attributed_checkouts'