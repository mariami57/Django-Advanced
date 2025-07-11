import time

from django.utils.deprecation import MiddlewareMixin


class MeasureTimeMiddleware(MiddlewareMixin):
    def process_request(self, request, *args, **kwargs):
        self.start_time = time.time()

    def process_response(self, request, response, *args, **kwargs):
        self.end_time = time.time()
        print(f"Request to {request.path} took {self.end_time - self.start_time} seconds.")
        return response

    def process_view(self, request, *args, **kwargs):
        print("Just before the view")

# def measure_time(get_response):
#     def middleware(request, *args, **kwargs):
#         start_time = time.time()
#         response = get_response(request, *args, **kwargs)
#         end_time = time.time()
#
#         print(f"Request to {request.path} took {end_time - start_time} seconds.")
#
#         return response
#     return middleware