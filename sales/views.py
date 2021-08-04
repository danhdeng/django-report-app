import pandas as pd

from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Sale
from .forms import SearchSaleForm

from .utils import get_customer_name_by_id, get_saleman_name_by_id, get_chart

# Create your views here.

def home_view(request):
    form=SearchSaleForm(request.POST or None)
    sales_df=None
    positions_df=None
    merge_df=None
    groupby_df=None
    chart=None
    if request.method =="POST":
        date_from=request.POST.get('date_from')
        date_to=request.POST.get('date_to')
        chart_type=request.POST.get('chart_type')
        sale_queryset=Sale.objects.filter(created__date__lte=date_to, created__date__gte=date_from)
        # print(queryset.values())
        # print(queryset.values_list())
        if len(sale_queryset) >0:
            sales_df = pd.DataFrame(sale_queryset.values())
            sales_df["customers_id"]=sales_df["customers_id"].apply(get_customer_name_by_id)
            sales_df["salesman_id"]=sales_df["salesman_id"].apply(get_saleman_name_by_id)
            sales_df["created"]=sales_df["created"].apply(lambda x: x.strftime('%y-%m-%d'))
            sales_df["updated"]=sales_df["updated"].apply(lambda x: x.strftime('%y-%m-%d'))
            sales_df.rename({"customers_id":"customer", "salesman_id": "sales person", "id":"sale_id"}, axis=1, inplace=True)
            
            positions_data=[]
            for sale in sale_queryset:
                for pos in sale.get_postions():
                    obj={
                        "position_id": pos.id,
                        "product": pos.product.name,
                        "price": pos.price,
                        "quantity": pos.quantity,
                        "sale_id" : pos.get_sale_id()
                    }
                    positions_data.append(obj)
            positions_df = pd.DataFrame(positions_data)
            merge_df=pd.merge(sales_df, positions_df, on="sale_id")
            groupby_df=merge_df.groupby('transaction_id', as_index=False)['price'].agg("sum")
            chart=get_chart(chart_type, groupby_df, labels=groupby_df["transaction_id"].values)
            sales_df=sales_df.to_html()
            positions_df=positions_df.to_html()
            merge_df=merge_df.to_html()
            groupby_df=groupby_df.to_html()

        else:
            print("no data")
        # pf2= pd.DataFrame(queryset.values_list())
        # print(pf2)

    context={
        "form":form,
        "sales_df": sales_df,
        "positions_df": positions_df,
        "merge_df": merge_df,
        "groupby_df": groupby_df,
        "chart": chart,
    }
    return render(request,'sales/home.html',context)

class SaleListView(ListView):
    
    model = Sale
    context_object_name = 'salelist'
    template_name='sales/sale_list.html'

    # def get_queryset(self):
    #      return Sale.objects.all()

class SaleDetailsView(DetailView):
    model= Sale
    context_object_name='sale'
    template_name='sales/sale_details.html'
