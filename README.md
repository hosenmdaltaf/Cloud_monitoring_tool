# Django AWS Monitoring App

This Django application provides monitoring capabilities for AWS EC2 instances, including CPU utilization, memory usage, disk usage, network traffic, and CPU credit balance. The app fetches data from AWS CloudWatch and provides visualizations and comparisons.

## Prerequisites

- Python 3.x
- Django 3.x or later
- AWS account with necessary permissions to access CloudWatch
- Plotly for graph generation
- Boto3 for AWS SDK for Python

## Setup

1. **Clone the repository**:

    ```bash
    git clone https://github.com/yourusername/your-repo.git
    cd your-repo
    ```

2. **Create a virtual environment**:

    ```bash
    python -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```

3. **Install dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

4. **Apply migrations**:

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5. **Create a superuser**:

    ```bash
    python manage.py createsuperuser
    ```

6. **Run the server**:

    ```bash
    python manage.py runserver
    ```

7. **Access the application**:

   Open your browser and navigate to `http://127.0.0.1:8000/` to access the app.

## Configuration

### AWS Credentials

- Users must update their profile with AWS credentials (Access Key ID, Secret Access Key, AWS region, and Instance ID) in the application's profile management interface.

### Key Features

- **AWS CloudWatch Metrics Retrieval**: Fetches metrics like CPU, memory, disk usage, network traffic, and CPU credits.
- **Data Storage**: Saves metrics to the database for historical comparisons.
- **Data Visualization**: Uses Plotly to visualize and compare metrics over time.
- **User Authentication**: Secure access to the application using Django's authentication system.

## Project Structure

- **account**: Contains user account-related views and templates.
- **monitoring_app**: Main application for fetching AWS metrics and displaying them.
- **templates**: HTML templates for rendering views.

## UML Diagrams

### Class Diagram

```plaintext
+------------------------+
|        Profile         |
+------------------------+
| user: OneToOneField    |
| location: CharField    |
| date_joined: DateTime  |
| last_login: DateTime   |
| aws_access_key_id: Text|
| aws_secret_access_key: Text|
| aws_region: Text       |
| instance_id: Text      |
+------------------------+

+------------------------+
|      MetricData        |
+------------------------+
| timestamp: DateTime    |
| cpu_utilization: Float |
| memory_utilization: Float|
| disk_utilization: Float|
| network_in: Float      |
| network_out: Float     |
| cpu_credit_balance: Float|
+------------------------+

+------------------------+
|       User             |
+------------------------+
| username: CharField    |
| email: EmailField      |
| password: CharField    |
| ...                    |
+------------------------+


