CREATE EXTENSION IF NOT EXISTS timescaledb;

CREATE TABLE readings (
    time       TIMESTAMPTZ      NOT NULL,
    device_id  TEXT             NOT NULL,
    metric     TEXT             NOT NULL,
    value      DOUBLE PRECISION NOT NULL
);

SELECT create_hypertable('readings', by_range('time', INTERVAL '1 day'));

CREATE INDEX readings_device_metric_time
    ON readings (device_id, metric, time DESC);
