from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('tableros/crear/', views.create_board, name='create_board'),
    path('tableros/<int:board_id>/', views.board_detail, name='board_detail'),
    path('tableros/<int:board_id>/listas/crear/', views.create_list, name='create_list'),

    path(
    'listas/<int:list_id>/tarjetas/crear/',
    views.create_card,
    name='create_card'
),
path('tarjetas/<int:card_id>/editar/', views.edit_card, name='edit_card'),
path('tarjetas/<int:card_id>/eliminar/', views.delete_card, name='delete_card'),
]