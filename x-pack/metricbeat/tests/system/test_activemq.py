import random
import string
import sys

import stomp
import unittest

from xpack_metricbeat import XPackTest
import metricbeat


class ActiveMqTest(XPackTest):
    COMPOSE_SERVICES = ['activemq']

    def get_activemq_module_config(self, metricset):
        return {
            'name': 'activemq',
            'metricsets': [metricset],
            'period': '5s',
            'hosts': self.get_hosts(),
            'path': '/api/jolokia/?ignoreErrors=true&canonicalNaming=false',
            'username': 'admin',
            'password': 'admin'
        }

    def get_stomp_host_port(self):
        host_port = self.compose_host(port='61613/tcp')
        s = host_port.split(':')
        return s[0], int(s[1])

    def destination_metrics_collected(self, destination_type, destination_name):
        if self.output_lines() == 0:
            return False

        output = self.read_output_json()
        for evt in output:
            if destination_type in evt['activemq'] and destination_name == evt['activemq'][destination_type]['name']:
                return True
        return False

    def verify_destination_metrics_collection(self, destination_type):
        self.render_config_template(modules=[self.get_activemq_module_config(destination_type)])
        proc = self.start_beat(home=self.beat_path)

        destination_name = ''.join(random.choice(string.ascii_lowercase) for i in range(10))

        conn = stomp.Connection([self.get_stomp_host_port()])
        conn.start()
        conn.connect(wait=True)
        conn.send('/{}/{}'.format(destination_type, destination_name), 'first message')
        conn.send('/{}/{}'.format(destination_type, destination_name), 'second message')

        self.wait_until(lambda: self.destination_metrics_collected(destination_type, destination_name))
        proc.check_kill_and_wait()
        self.assert_no_logged_warnings()

        output = self.read_output_json()

        passed = False
        for evt in output:
            if destination_name == evt['activemq'][destination_type]['name']:
                assert 2 == evt['activemq'][destination_type]['messages']['enqueue']['count']
                assert 0 < evt['activemq'][destination_type]['messages']['size']['avg']
                if 'queue' == destination_type:
                    assert 0 < evt['activemq'][destination_type]['size']
                self.assert_fields_are_documented(evt)
                passed = True

        conn.disconnect()
        assert passed

    @unittest.skipUnless(metricbeat.INTEGRATION_TESTS, 'integration test')
    def test_broker_metrics_collected(self):
        self.render_config_template(modules=[self.get_activemq_module_config('broker')])
        proc = self.start_beat(home=self.beat_path)
        self.wait_until(lambda: self.output_lines() > 0)
        proc.check_kill_and_wait()
        self.assert_no_logged_warnings()

        output = self.read_output_json()

        for evt in output:
            assert 'name' in evt['activemq']['broker']
            assert 'pct' in evt['activemq']['broker']['memory']['broker']
            assert 'count' in evt['activemq']['broker']['producers']
            assert 'count' in evt['activemq']['broker']['consumers']
            self.assert_fields_are_documented(evt)

    @unittest.skipUnless(metricbeat.INTEGRATION_TESTS, 'integration test')
    def test_queue_metrics_collected(self):
        self.verify_destination_metrics_collection('queue')

    @unittest.skipUnless(metricbeat.INTEGRATION_TESTS, 'integration test')
    def test_topic_metrics_collected(self):
        self.verify_destination_metrics_collection('topic')


class TestRelease5130(ActiveMqTest):
    COMPOSE_ENV = {'ACTIVEMQ_VERSION': '5.13.0'}
