from __future__ import absolute_import, unicode_literals

from unittest import TestCase

from mock import Mock

from eb_sqs import settings
from eb_sqs.decorators import task
from eb_sqs.worker.worker import Worker
from eb_sqs.worker.worker_factory import WorkerFactory


@task()
def dummy_task(msg):
    # type: (unicode) -> None
    if not msg:
        raise Exception('No message')

@task()
def dummy_retry_task(msg):
    # type: (unicode) -> None
    if dummy_retry_task.retry_num == 0:
        dummy_retry_task.retry()
    else:
        if not msg:
            raise Exception('No message')


class DecoratorsTest(TestCase):
    def setUp(self):
        self.worker_mock = Mock(autospec=Worker)

        factory_mock = Mock(autospec=WorkerFactory)
        factory_mock.create.return_value = self.worker_mock
        settings.WORKER_FACTORY = factory_mock

    def test_delay_decorator(self):
        dummy_task.delay('Hello World!')
        self.worker_mock.delay.assert_called_once()

    def test_retry_decorator(self):
        dummy_retry_task.delay('Hello World!')
        self.worker_mock.delay.assert_called_once()
