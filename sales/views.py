import pandas as pd

from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Sale
from .forms import SearchSaleForm
from reports.forms import ReportForm

from .utils import get_customer_name_by_id, get_saleman_name_by_id, get_chart

# Create your views here.
@login_required
def home_view(request):
    search_form=SearchSaleForm(request.POST or None)
    report_form=ReportForm
    sales_df=None
    positions_df=None
    merge_df=None
    groupby_df=None
    chart=None
    no_data=None
    if request.method =="POST":
        date_from=request.POST.get('date_from')
        date_to=request.POST.get('date_to')
        chart_type=request.POST.get('chart_type')
        result_by=request.POST.get('result_by')
        sale_queryset=Sale.objects.filter(created__date__lte=date_to, created__date__gte=date_from)
        if len(sale_queryset) >0:
            sales_df = pd.DataFrame(sale_queryset.values())
            sales_df["customer_id"]=sales_df["customer_id"].apply(get_customer_name_by_id)
            sales_df["salesman_id"]=sales_df["salesman_id"].apply(get_saleman_name_by_id)
            sales_df["created"]=sales_df["created"].apply(lambda x: x.strftime('%y-%m-%d'))
            sales_df["updated"]=sales_df["updated"].apply(lambda x: x.strftime('%y-%m-%d'))
            sales_df.rename({"customer_id":"customer", "salesman_id": "sales person", "id":"sale_id"}, axis=1, inplace=True)
            
            positions_data=[]
            for sale in sale_queryset:
                for pos in sale.get_postions():
                    obj={
                        "position_id": pos.id,
                        "product": pos.product.name,
                        "price": pos.price,
                        "quantity": pos.quantity,
                        "sale_id" : pos.get_sales_id()
                    }
                    positions_data.append(obj)
            positions_df = pd.DataFrame(positions_data)
            merge_df=pd.merge(sales_df, positions_df, on="sale_id")
            groupby_df=merge_df.groupby('transaction_id', as_index=False)['price'].agg("sum")
            #chart=get_chart(chart_type, groupby_df, labels=groupby_df["transaction_id"].values)
            chart=get_chart(chart_type, sales_df, result_by)
            sales_df=sales_df.to_html()
            positions_df=positions_df.to_html()
            merge_df=merge_df.to_html()
            groupby_df=groupby_df.to_html()

        else:
            no_data="No data is avaiable in this date range"

    context={
        "search_form":search_form,
        "sales_df": sales_df,
        "positions_df": positions_df,
        "merge_df": merge_df,
        "groupby_df": groupby_df,
        "chart": chart,
        "report_form": report_form,
        "no_data": no_data,

    }
    return render(request,'sales/home.html',context)


class SaleListView(LoginRequiredMixin,ListView):
    
    model = Sale
    context_object_name = 'salelist'
    template_name='sales/sale_list.html'

    # def get_queryset(self):
    #      return Sale.objects.all()

class SaleDetailsView(LoginRequiredMixin,DetailView):
    model= Sale
    context_object_name='sale'
    template_name='sales/sale_details.html'
