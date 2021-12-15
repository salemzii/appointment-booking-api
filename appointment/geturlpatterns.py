from Appointments.settings import *
from Appointments.urls import urlpatterns


print(dir(urlpatterns))

for url in urlpatterns:
    print(url)