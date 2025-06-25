import boto3
from datetime import datetime, timedelta
from django.shortcuts import render
from django.http import JsonResponse
from .models import MetricData
from django.contrib.auth.decorators import login_required

import plotly.graph_objects as go
from plotly.subplots import make_subplots    


def get_cloudwatch_metrics(aws_access_key_id, aws_secret_access_key, aws_region, namespace, metric_name, dimensions, start_time, end_time, period, statistics):
    # Initialize Boto3 session using the provided credentials
    boto3.setup_default_session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=aws_region
    )

    # Initialize Boto3 client for CloudWatch
    cloudwatch = boto3.lcient('cloudwatch')

    # Fetch the CloudWatch metrics
    response = cloudwatch.get_metric_statistics(
        Namespace=namespace,
        MetricName=metric_name,
        Dimensions=dimensions,
        StartTime=start_time,
        EndTime=end_time, 
        Period=period,
        Statistics=statistics
    )
    
    return response['Datapoints']


def get_metrics(dimensions, start_time, end_time, period, request):
    profile = request.user.profile

    metrics = {
        "cpu_utilization": get_cloudwatch_metrics(
            aws_access_key_id=profile.aws_access_key_id,
            aws_secret_access_key=profile.aws_secret_access_key,
            aws_region=profile.aws_region,
            namespace='AWS/EC2',
            metric_name='CPUUtilization',
            dimensions=dimensions,
            start_time=start_time,
            end_time=end_time,
            period=period,
            statistics=['Average']
        ),
        "memory_utilization": get_cloudwatch_metrics(
            aws_access_key_id=profile.aws_access_key_id,
            aws_secret_access_key=profile.aws_secret_access_key,
            aws_region=profile.aws_region,
            namespace='CWAgent',
            metric_name='mem_used_percent',
            dimensions=dimensions,
            start_time=start_time,
            end_time=end_time,
            period=period,
            statistics=['Average']
        ),
        "disk_utilization": get_cloudwatch_metrics(
            aws_access_key_id=profile.aws_access_key_id,
            aws_secret_access_key=profile.aws_secret_access_key,
            aws_region=profile.aws_region,
            namespace='CWAgent',
            metric_name='disk_used_percent',
            dimensions=dimensions,
            start_time=start_time,
            end_time=end_time,
            period=period,
            statistics=['Average']
        ),
        "network_in": get_cloudwatch_metrics(
            aws_access_key_id=profile.aws_access_key_id,
            aws_secret_access_key=profile.aws_secret_access_key,
            aws_region=profile.aws_region,
            namespace='AWS/EC2',
            metric_name='NetworkIn',
            dimensions=dimensions,
            start_time=start_time,
            end_time=end_time,
            period=period,
            statistics=['Sum']
        ),
        "network_out": get_cloudwatch_metrics(
            aws_access_key_id=profile.aws_access_key_id,
            aws_secret_access_key=profile.aws_secret_access_key,
            aws_region=profile.aws_region,
            namespace='AWS/EC2',
            metric_name='NetworkOut',
            dimensions=dimensions,
            start_time=start_time,
            end_time=end_time,
            period=period,
            statistics=['Sum']
        ),
        "cpu_credit_balance": get_cloudwatch_metrics(
            aws_access_key_id=profile.aws_access_key_id,
            aws_secret_access_key=profile.aws_secret_access_key,
            aws_region=profile.aws_region,
            namespace='AWS/EC2',
            metric_name='CPUCreditBalance',
            dimensions=dimensions,
            start_time=start_time,
            end_time=end_time,
            period=period,
            statistics=['Sum']
        )
    }
    return metrics

@login_required
def get_aws_metrics(request):
    # Fetch the user's profile and instance ID
    profile = request.user.profile
    instance_id = profile.instance_id

    # Define the time range and period
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=1)
    period = 3600

    # Define dimensions (e.g., instance ID for EC2 metrics)
    dimensions = [{'Name': 'InstanceId', 'Value': instance_id}]

    # Fetch metrics using the now global get_metrics function
    metrics = get_metrics(dimensions, start_time, end_time, period, request)

    # Return the metrics along with the AWS credentials
    return JsonResponse({
        'aws_access_key_id': profile.aws_access_key_id,
        'aws_secret_access_key': profile.aws_secret_access_key,
        'aws_region': profile.aws_region,
        'instance_id': instance_id,
        'metrics': metrics
    })

def get_latest_metric(datapoints):
    if not datapoints:
        return None
    average = datapoints[-1].get('Average')
    sum_val = datapoints[-1].get('Sum')
    return average if average is not None else sum_val

@login_required
def retrieve_and_save_metrics(request):
    try:
        profile = request.user.profile
        instance_id = profile.instance_id
        
        # Define the time range and period
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(minutes=5)
        period = 60

        # Define dimensions (e.g., instance ID for EC2 metrics)
        dimensions = [{'Name': 'InstanceId', 'Value': instance_id}]

        # Fetch metrics using the get_metrics function
        metrics = get_metrics(dimensions, start_time, end_time, period, request)

        # Save metrics to the database 
        MetricData.objects.create(
            cpu_utilization=get_latest_metric(metrics['cpu_utilization']),
            memory_utilization=get_latest_metric(metrics['memory_utilization']),
            disk_utilization=get_latest_metric(metrics['disk_utilization']),
            network_in=get_latest_metric(metrics['network_in']),
            network_out=get_latest_metric(metrics['network_out']),
            cpu_credit_balance=get_latest_metric(metrics['cpu_credit_balance'])
        )

        return render(request, 'monitoring_app/dashboard.html', {'data': metrics})
    
    except Exception as e:
        print("Error: ", str(e))
        return JsonResponse({"error": str(e)}, status=500)

def compare_metrics(current, previous):
    def calculate_difference(current_value, previous_value):
        if current_value is None or previous_value is None:
            return None
        if previous_value == 0:
            return float('inf') if current_value != 0 else 0
        return ((current_value - previous_value) / previous_value) * 100

    comparison = {
        "cpu_utilization": {
            "current_value": current.cpu_utilization,
            "previous_value": previous.cpu_utilization,
            "difference": calculate_difference(current.cpu_utilization, previous.cpu_utilization)
        },
        "memory_utilization": {
            "current_value": current.memory_utilization,
            "previous_value": previous.memory_utilization,
            "difference": calculate_difference(current.memory_utilization, previous.memory_utilization)
        },
        "disk_utilization": {
            "current_value": current.disk_utilization,
            "previous_value": previous.disk_utilization,
            "difference": calculate_difference(current.disk_utilization, previous.disk_utilization)
        },
        "network_in": {
            "current_value": current.network_in,
            "previous_value": previous.network_in,
            "difference": calculate_difference(current.network_in, previous.network_in)
        },
        "network_out": {
            "current_value": current.network_out,
            "previous_value": previous.network_out,
            "difference": calculate_difference(current.network_out, previous.network_out)
        },
        "cpu_credit_balance": {
            "current_value": current.cpu_credit_balance,
            "previous_value": previous.cpu_credit_balance,
            "difference": calculate_difference(current.cpu_credit_balance, previous.cpu_credit_balance)
        }
    }
    return comparison

def generate_comparison_graphs(comparison_results):
    fig = make_subplots(rows=2, cols=3, subplot_titles=("CPU Utilization", "Memory Utilization", "Disk Utilization", "Network In", "Network Out", "CPU Credit Balance"))

    metric_names = ["cpu_utilization", "memory_utilization", "disk_utilization", "network_in", "network_out", "cpu_credit_balance"]
    current_values = [comparison_results[metric]["current_value"] for metric in metric_names]
    previous_values = [comparison_results[metric]["previous_value"] for metric in metric_names]

    # Plot each metric
    for i, metric in enumerate(metric_names):
        row = i // 3 + 1
        col = i % 3 + 1
        fig.add_trace(go.Bar(name='Current', x=[metric], y=[current_values[i]], marker_color='blue'), row=row, col=col)
        fig.add_trace(go.Bar(name='Previous', x=[metric], y=[previous_values[i]], marker_color='red'), row=row, col=col)

    fig.update_layout(height=600, width=900, title_text="Metric Comparison", barmode='group')

    graph_div = fig.to_html(full_html=False)
    return graph_div


def compare_metrics_view(request):
    try:
        # Retrieve the latest two entries from the database
        latest_metrics = MetricData.objects.order_by('-timestamp')[:2]

        if len(latest_metrics) < 2:
            return JsonResponse({"error": "Not enough data to compare"}, status=400)

        current_metrics = latest_metrics[0]
        previous_metrics = latest_metrics[1]

        comparison_results = compare_metrics(current_metrics, previous_metrics)

        print('--------comparison_results-----------')
        print(comparison_results)
        graph_div = generate_comparison_graphs(comparison_results)

        return render(request, 'monitoring_app/compare_metrics.html', {'comparison_results': comparison_results,'graph_div': graph_div})

    except Exception as e:
        print("Error: ", str(e))
        return JsonResponse({"error": str(e)}, status=500)
    


