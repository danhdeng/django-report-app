import uuid, base64
import matplotlib.pyplot as plt
import seaborn
from customers.models import Customer
from profiles.models import Profile
from io import BytesIO

def generate_code():
    return  str(uuid.uuid4()).replace('-','').upper()[:12]

def get_customer_name_by_id(val):
    return Customer.objects.get(id=val)

def get_saleman_name_by_id(val):
    profile = Profile.objects.get(id=val)
    return profile

def get_graph():
    buffer=BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png=buffer.getvalue()
    graph =base64.b64encode(image_png)
    graph=graph.decode('utf-8')
    buffer.close()
    return graph

def get_chart(chart_type, data, **kwargs):
    plt.switch_backend('AGG')
    fig=plt.figure(figsize=(10,4))
    if(chart_type=='#1'):
        print("Bar Chart")
        # plt.bar(data["transaction_id"], data["price"])
        seaborn.barplot(x="transaction_id", y="price", data=data)
    elif(chart_type=='#2'):
        print("Pie Chart")
        labels=kwargs.get("labels")
        plt.pie(data=data, x="price", labels=labels)
    elif(chart_type=='#3'):
        print("Line Chart")
        plt.plot(data["transaction_id"], data["price"], linestyle="dashed", color='red', marker='o')
    else:
        print("Unable to identify the chart")
    plt.tight_layout()
    chart= get_graph()
    return chart