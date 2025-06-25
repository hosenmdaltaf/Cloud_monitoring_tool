from django.test import TestCase

# Create your tests here.
import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from .views import get_cloudwatch_metrics, get_metrics

class TestMonitoringSystem(unittest.TestCase):

    @patch('your_module.boto3.client')
    def test_get_cloudwatch_metrics(self, mock_boto_client):
        # Mock AWS CloudWatch client
        mock_client = MagicMock()
        mock_boto_client.return_value = mock_client
        mock_client.get_metric_statistics.return_value = {
            'Datapoints': [{'Timestamp': datetime.utcnow(), 'Average': 50.0}]
        }

        # Test data
        aws_access_key_id = 'test_access_key'
        aws_secret_access_key = 'test_secret_key'
        aws_region = 'us-west-2'
        namespace = 'AWS/EC2'
        metric_name = 'CPUUtilization'
        dimensions = [{'Name': 'InstanceId', 'Value': 'i-1234567890abcdef0'}]
        start_time = datetime.utcnow() - timedelta(days=1)
        end_time = datetime.utcnow()
        period = 3600
        statistics = ['Average']

        # Call the function
        result = get_cloudwatch_metrics(aws_access_key_id, aws_secret_access_key, aws_region, namespace, metric_name, dimensions, start_time, end_time, period, statistics)

        # Assertions
        mock_boto_client.assert_called_once_with('cloudwatch')
        mock_client.get_metric_statistics.assert_called_once_with(
            Namespace=namespace,
            MetricName=metric_name,
            Dimensions=dimensions,
            StartTime=start_time,
            EndTime=end_time,
            Period=period,
            Statistics=statistics
        )
        self.assertEqual(result, [{'Timestamp': datetime.utcnow(), 'Average': 50.0}])

    @patch('your_module.get_cloudwatch_metrics')
    def test_get_metrics(self, mock_get_cloudwatch_metrics):
        # Mock response for get_cloudwatch_metrics
        mock_get_cloudwatch_metrics.return_value = [{'Timestamp': datetime.utcnow(), 'Average': 50.0}]

        # Test data
        dimensions = [{'Name': 'InstanceId', 'Value': 'i-1234567890abcdef0'}]
        start_time = datetime.utcnow() - timedelta(days=1)
        end_time = datetime.utcnow()
        period = 3600
        mock_request = MagicMock()
        mock_request.user.profile.aws_access_key_id = 'test_access_key'
        mock_request.user.profile.aws_secret_access_key = 'test_secret_key'
        mock_request.user.profile.aws_region = 'us-west-2'

        # Call the function
        result = get_metrics(dimensions, start_time, end_time, period, mock_request)

        # Assertions
        self.assertIn('cpu_utilization', result)
        self.assertEqual(result['cpu_utilization'], [{'Timestamp': datetime.utcnow(), 'Average': 50.0}])

if __name__ == '__main__':
    unittest.main()
