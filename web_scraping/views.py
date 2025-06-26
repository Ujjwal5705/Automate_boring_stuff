from django.shortcuts import render, redirect
from dal import autocomplete
from .models import Stock, Stockdata
from .forms import StockForm
from django.http import HttpResponse
from .utils import scrap_stock_data
from django.contrib import messages

# Create your views here.


def stock(request):
    if request.method == 'POST':
        form = StockForm(request.POST)
        if form.is_valid():
            stock_name = form.cleaned_data['stock']
            stock_object = Stock.objects.filter(name=stock_name)[0]
            symbol = f"{stock_object.symbol}"
            exchange = f"{stock_object.exchange}"
            stock_response = scrap_stock_data(symbol, exchange)

            if stock_response is not None:
                try:
                    stock_data = Stockdata.objects.get(stock=stock_object)
                except:
                    stock_data = Stockdata(stock=stock_object)

                stock_data.current_price=stock_response['stock_price']
                stock_data.price_change=stock_response['price_change']
                stock_data.percent_change=stock_response['percent_change']
                stock_data.previous_close=stock_response['previous_close']
                stock_data.week_52_high=stock_response['week_52_high']
                stock_data.week_52_low=stock_response['week_52_low']
                stock_data.market_cap=stock_response['market_cap']
                stock_data.pe_ratio=stock_response['pe_ratio']
                stock_data.dividend_yield=stock_response['dividend_yield']
                stock_data.save()

                return redirect('stock_detail', stock_data.pk)
            else:
                messages.error(request, f'Could not fetch the data for {stock_name} - {symbol}')
                return redirect('stock')
        else:
            print('Form is not Valid')
    else:
        form = StockForm()
        context = {
            'form': form,
        }
        return render(request, 'stockanalysis/stocks.html', context)


class StockAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Stock.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs


def stockdetail(request, pk):
    stock_data = Stockdata.objects.get(pk=pk)

    context = {
        'stock_data': stock_data,
    }
    return render(request, 'stockanalysis/stockdetail.html', context)