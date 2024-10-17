# views.py atau bisa diletakkan di dalam manajemen command (jika ingin dijalankan sebagai script)

from django.db.models import Count
from .models import Client, Odp
from datetime import date

def update_odp_data():
    # Menghitung jumlah client yang terhubung ke setiap Odp berdasarkan 'connectto'
    client_counts = Client.objects.values('connectto').annotate(client_count=Count('id'))

    # Iterasi setiap Odp dan update jumlah portFilled dan portRemaining
    for client_count in client_counts:
        odp_id = client_count['connectto']
        port_filled = client_count['client_count']

        # Coba cari Odp yang sesuai dengan 'connectto' dari tabel client
        try:
            odp = Odp.objects.get(odpId=odp_id)
            odp.portFilled = port_filled
            odp.portRemaining = odp.total_port - port_filled
            odp.save()
        except Odp.DoesNotExist:
            continue