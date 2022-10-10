class Searchmixin(object):
	def sindex(self):
		queryset =self.request.GET.get('q')
		return httpResponse(query)

	def perf(self, query):
		if query is not None:
			post = self.objects.filter(
				Q(title__icontains=query)
				)
		return render(request, 'blog/home.html', post)