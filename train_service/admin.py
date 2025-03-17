from django.contrib import admin

from train_service.models import (TrainType,
                                 Train,
                                 Order,
                                 Crew,
                                 Journey,
                                 Ticket,
                                 Route,
                                 Station,
                                 City)

admin.site.register(TrainType)
admin.site.register(Train)
admin.site.register(Order)
admin.site.register(Crew)
admin.site.register(Journey)
admin.site.register(Ticket)
admin.site.register(Route)
admin.site.register(Station)
admin.site.register(City)