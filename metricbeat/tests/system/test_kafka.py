import os
import metricbeat
import unittest
from nose.plugins.attrib import attr
from nose.plugins.skip import SkipTest


class KafkaTest(metricbeat.BaseTest):
    COMPOSE_SERVICES = ['kafka']
    COMPOSE_ADVERTISED_HOST = True
    COMPOSE_ADVERTISED_PORT = "9092/tcp"

    VERSION = "2.0.0"

    PRODUCER_USERNAME = "producer"
    PRODUCER_PASSWORD = "producer-secret"

    USERNAME = "stats"
    PASSWORD = "test-secret"

    @unittest.skipUnless(metricbeat.INTEGRATION_TESTS, "integration test")
    def test_partition(self):
        """
        kafka partition metricset test
        """

        self.create_topic()

        self.render_config_template(modules=[{
            "name": "kafka",
            "metricsets": ["partition"],
            "hosts": self.get_hosts(),
            "period": "1s",
            "version": self.VERSION,
            "username": self.USERNAME,
            "password": self.PASSWORD,
        }])
        proc = self.start_beat()
        self.wait_until(lambda: self.output_lines() > 0, max_timeout=20)
        proc.check_kill_and_wait()

        output = self.read_output_json()
        self.assertTrue(len(output) >= 1)
        evt = output[0]
        print(evt)

        self.assert_fields_are_documented(evt)

    def create_topic(self):
        from kafka import KafkaProducer

        producer = KafkaProducer(
            bootstrap_servers=self.get_hosts()[0],
            security_protocol="SASL_PLAINTEXT",
            sasl_mechanism="PLAIN",
            sasl_plain_username=self.PRODUCER_USERNAME,
            sasl_plain_password=self.PRODUCER_PASSWORD,
            retries=20, retry_backoff_ms=500)
        producer.send('foobar', b'some_message_bytes')

    @classmethod
    def get_hosts(cls):
        return [cls.compose_host(port=cls.COMPOSE_ADVERTISED_PORT)]


class Kafka_1_1_0_Test(KafkaTest):
    COMPOSE_ENV = {"KAFKA_VERSION": "1.1.0"}
    VERSION = "1.1.0"


class Kafka_0_10_2_Test(KafkaTest):
    COMPOSE_ENV = {"KAFKA_VERSION": "0.10.2.2"}
    VERSION = "0.10.2.2"
