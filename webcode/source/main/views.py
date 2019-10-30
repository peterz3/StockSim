from django.views.generic import TemplateView
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.utils.crypto import get_random_string
from django.utils.decorators import method_decorator
from django.utils.http import is_safe_url
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import View, FormView
from django.conf import settings
import requests
from django.urls import reverse

from django.views.generic import View, FormView
from .forms import StocksForm
from django.shortcuts import get_object_or_404, redirect

class IndexPageView(TemplateView, FormView):
	template_name = 'main/index.html'
	sym = "hello"
	#form = StocksForm()

	@staticmethod
	def get_form_class(**kwargs):
		#return (self, form):
		#context = super().get_context_data(**kwargs)
		#context['symbol'] = 'APPL'
		return StocksForm

	def form_valid(self, form):
		request = self.request
		self.sym = form.cleaned_data['stockdata']
		return redirect('index', symbol=form.cleaned_data['stockdata'])

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		
		# This is just an example of how to query the db to pull information.
		# To use this we just need
		#sql = 'SELECT * FROM Stock WHERE TickerSymbol=?'
		#arg = ('APPL',)
		#record = common.db_helper.db_query(sql, arg)
		#if record:
		#	context['symbol'] = record['TickerSymbol']
		#else:

		if self.request.get_full_path() == '/':
			context['symbol'] = ''
		else:
			url = self.request.get_full_path()
			context['symbol'] = url.split('?stockdata=')[1]
		return context


'''
	def get_stocks(self, request):
		#context = super().get_context_data(**kwargs)
		#context = super().get_context_data(**kwargs)
		#data = request.session.pop('data', None)

		#print("getting " + str(kwargs.get('data')))
		#context['symbol'] = self.form_input
		#context['symbol'] = data
		
		#add entries to context
		#form = get_form_class()
		form = StocksForm()
		context = {}
		print("hello")
		if request.method == 'POST':
			form = StocksForm(request.POST)
			if form.is_valid():
				print(form.cleaned_data['stockdata'])
				context['symbol'] = form.cleaned_data['stockdata']
				return context
		else:
			form = StocksForm()
		
		return render(request, 'index', {'form' : form})
'''

'''
	
	def form_valid(self, form ):
		print(form.cleaned_data['stockdata'])
		#context = super().get_context_data(**kwargs)
		#context['symbol'] = 'APPL'
		data = {'symbol'  : form.cleaned_data['stockdata'] }
		
		#data = self.request.session.pop('data', None)
		#self.get_context_data(data =  form.cleaned_data['stockdata'])
		#data['stock'] = form.cleaned_data['stockdata']
		#self.request.session['data'] = data	


		#red_ =  redirect('index')
		#red_.symbol = form.cleaned_data['stockdata']
		#request.session['data'] = data	
		#get_context_data(request, data = data)
		#return render(self.request,'main/index.html', data)
		return redirect('index', symbol=form.cleaned_data['stockdata']  )
		'''

class ChangeLanguageView(TemplateView):
    template_name = 'main/change_language.html'
