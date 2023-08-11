from typing import Tuple
from dataclasses import asdict

from jinja2 import Environment, FileSystemLoader
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment

from utils.config import StreamJobConfig, ClickTopicConfig,CheckoutTopicConfig,ApplicationUsersTableConfig,ApplicationAttributedCheckoutsTableConfig

def get_execution_environment(
        config: StreamJobConfig
) -> Tuple[StreamExecutionEnvironment, StreamTableEnvironment]:
    s_env = StreamExecutionEnvironment.get_execution_environment()
    for jar in config.jars:
        s_env.add_jars(jar)
    
    # start checkpoint every 10s
    s_env.enable_checkpointing(config.checkpoint_interval * 1000)

    #ensure 5s pause between checkpoints
    s_env.get_checkpoint_config().set_min_pause_between_checkpoints(
        config.checkpoint_pause * 5000
    )

    # timeout of checkpoint
    s_env.get_checkpoint_config().set_checkpoint_timeout(
        config.checkpoint_timeout * 1000
    )

    execution_config = s_env.get_config()
    execution_config.set_parallelism(config.parallelism)
    t_env = StreamTableEnvironment.create(s_env)
    job_config = t_env.get_config().get_configuration()
    job_config.set_string("pipeline.name", config.job_name)
    return s_env, t_env


def get_sql_query(
        entity: str,
        type: str = "source",
        template_env: Environment = Environment(loader=FileSystemLoader("src/")),
) -> str:
    config_map = {
        'clicks': ClickTopicConfig(),
        'checkouts': CheckoutTopicConfig(),
        'users': ApplicationUsersTableConfig(),
        'attributed_checkouts': ApplicationUsersTableConfig(),
        'attribute_checkouts': ApplicationAttributedCheckoutsTableConfig(),
    }
    return template_env.get_template(f"{type}/{entity}.sql").render(
        asdict(config_map.get(entity))
    )

def run_checkout_attribution_job(
        t_env: StreamTableEnvironment,
        get_sql_query=get_sql_query,
) -> None:
    #create source DDLs
    t_env.execute_sql(get_sql_query(entity='clicks'))
    t_env.execute_sql(get_sql_query(entity='checkouts'))
    t_env.execute_sql(get_sql_query(entity='users'))

    #create sink DDL
    t_env.execute_sql(get_sql_query(entity='attributed_checkouts', type='sink'))

    # run processing query
    stmt_set = t_env.create_statement_set()
    stmt_set.add_insert_sql(get_sql_query(entity='attribute_checkouts', type='process'))

    checkout_attribution_job = stmt_set.execute()
    print(
        f"""
        Async attributed checkouts sink job status: {checkout_attribution_job.get_job_client().get_job_status()}
        """
    )



    pass

if __name__ == '__main__':
    _, t_env = get_execution_environment(StreamJobConfig())
    run_checkout_attribution_job(t_env)