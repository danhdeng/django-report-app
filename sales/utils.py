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

def get_result_by(result_by):
    if(result_by=='#1'):
        return "transaction_id"
    elif(result_by=='#2'):
        return "created"
    

def get_chart(chart_type, data, result_by, **kwargs):
    plt.switch_backend('AGG')
    fig=plt.figure(figsize=(10,4))
    key=get_result_by(result_by)
    groupby_data=data.groupby(data[key], as_index=False)['total_price'].agg("sum")
    # groupby_data=data
    if(chart_type=='#1'):
        # plt.bar(data["transaction_id"], data["price"])
        seaborn.barplot(x=key, y="total_price", data=groupby_data)
    elif(chart_type=='#2'):
        labels=kwargs.get("labels")
        plt.pie(data=groupby_data, x="total_price", labels=groupby_data[key].values)
    elif(chart_type=='#3'):
        plt.plot(groupby_data[key], groupby_data["total_price"], linestyle="dashed", color='red', marker='o')
    else:
        print("Unable to identify the chart")
    plt.tight_layout()
    chart= get_graph()
    return chart