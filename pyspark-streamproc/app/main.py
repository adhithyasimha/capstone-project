import os
import json
import logging
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    IntegerType,
    LongType,
    BooleanType,
)


def main() -> None:
    bootstrap = os.getenv("KAFKA_BOOTSTRAP", "kafka-1-dev:9092")
    topic = os.getenv("KAFKA_TOPIC", "capstone-logi")

    spark = (
        SparkSession.builder
        .appName("capstone-logi-stream")
        .config("spark.sql.shuffle.partitions", "2")
        .getOrCreate()
    )

    # Reduce Spark log verbosity
    try:
        spark.sparkContext.setLogLevel("WARN")
    except Exception:
        pass

    # Read raw Kafka records
    raw = (
        spark.readStream
        .format("kafka")
        .option("kafka.bootstrap.servers", bootstrap)
        .option("subscribe", topic)
        .option("startingOffsets", "latest")
        .option("failOnDataLoss", "false")
        .load()
    )

    # JSON schema matching handleLogi.go and capstoneLogi.ts
    event_schema = StructType([
        StructField("type", StringType(), True),
        StructField("srn", StringType(), True),
        StructField("questionID", IntegerType(), True),
        StructField("ts", LongType(), True),
        StructField("content", StringType(), True),
        StructField("offset", IntegerType(), True),
        StructField("numCharacters", IntegerType(), True),
        StructField("isPaste", BooleanType(), True),
    ])

    # Parse JSON payload into typed columns and include basic metadata
    events = (
        raw.select(
            from_json(col("value").cast("string"), event_schema).alias("event"),
            col("topic"),
            col("partition"),
            col("offset"),
            col("timestamp"),
        )
        .select("event.*", "topic", "partition", "offset", "timestamp")
    )

    logger = logging.getLogger("capstone-logi-stream")
    logging.basicConfig(level=os.getenv("PY_LOG_LEVEL", "INFO"))

    def write_batch(batch_df, batch_id: int) -> None:
        # Basic batch diagnostics
        try:
            count = batch_df.count()
        except Exception as exc:
            logger.error("[batch %s] count failed: %s", batch_id, exc)
            return
        logger.info("[batch %s] rows=%s", batch_id, count)
        if count == 0:
            return

        # Connect to Redis (single node or cluster)
        try:
            import redis
        except Exception as exc:  # pragma: no cover
            logger.error("[redis] import failed: %s", exc)
            return

        cluster_nodes = os.getenv("REDIS_CLUSTER_NODES", "").strip()
        if cluster_nodes:
            startup_nodes = []
            for node in cluster_nodes.split():
                host, _, port = node.partition(":")
                startup_nodes.append({"host": host, "port": int(port or 6379)})
            try:
                r = redis.cluster.RedisCluster(startup_nodes=startup_nodes, decode_responses=True)
            except Exception as exc:  # pragma: no cover
                logger.error("[redis] cluster connect failed: %s", exc)
                return
        else:
            host = os.getenv("REDIS_HOST", "redis-dev")
            port = int(os.getenv("REDIS_PORT", "6379"))
            try:
                r = redis.Redis(host=host, port=port, decode_responses=True)
            except Exception as exc:  # pragma: no cover
                logger.error("[redis] single-node connect failed: %s", exc)
                return

        # Verify Redis connectivity
        try:
            pong = r.ping()
            logger.info("[batch %s] redis ping=%s", batch_id, pong)
        except Exception as exc:
            logger.error("[batch %s] redis ping failed: %s", batch_id, exc)
            return

        # Iterate events and update JSON per key `srn|questionID`
        # Fields: total_actions, latest_log_ts, paste_count, deletion_count, compilation_count, submission_count
        updated = 0
        for row in batch_df.select("srn", "questionID", "ts", "isPaste", "type").toLocalIterator():
            ev = row.asDict(recursive=True)
            srn = ev.get("srn")
            qid = ev.get("questionID")
            if srn is None or qid is None:
                continue
            key = f"{srn}|{qid}"

            try:
                current_raw = r.get(key)
            except Exception:
                current_raw = None

            if current_raw:
                try:
                    state = json.loads(current_raw)
                except Exception:
                    state = {}
            else:
                state = {}

            # Initialize if missing
            state.setdefault("total_actions", 0)
            state.setdefault("latest_log_ts", 0)
            state.setdefault("paste_count", 0)
            state.setdefault("deletion_count", 0)
            state.setdefault("compilation_count", 0)
            state.setdefault("submission_count", 0)

            # Apply updates
            state["total_actions"] += 1

            ts = ev.get("ts") or 0
            if isinstance(ts, (int, float)) and ts > (state.get("latest_log_ts") or 0):
                state["latest_log_ts"] = int(ts)

            if ev.get("isPaste"):
                state["paste_count"] += 1

            etype = (ev.get("type") or "").lower()
            if etype == "delete":
                state["deletion_count"] += 1
            elif etype == "run":
                state["compilation_count"] += 1
            elif etype == "submission":
                state["submission_count"] += 1

            try:
                r.set(key, json.dumps(state, separators=(",", ":")))
                updated += 1
            except Exception as exc:  # pragma: no cover
                logger.error("[redis] set failed for key=%s: %s", key, exc)

        logger.info("[batch %s] updated_keys=%s", batch_id, updated)

    # Persist Kafka offsets/state so we don't re-read on restart
    checkpoint_dir = os.getenv("CHECKPOINT_DIR", "")
    writer = events.writeStream.foreachBatch(write_batch)
    if checkpoint_dir:
        writer = writer.option("checkpointLocation", checkpoint_dir)
    query = writer.start()

    query.awaitTermination()


if __name__ == "__main__":
    main()


