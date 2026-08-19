from django.urls import path
from .views import (
    ManageDocumentsView,
    AddDocumentView,
    EditDocumentView,
    DeleteDocumentView,
    ManagePlacementsView,
    AddPlacementView,
    EditPlacementView,
    DeletePlacementView,
    ManageLabsView,
    AddLabView,
    EditLabView,
    DeleteLabView,
)

app_name = 'core_admin'

urlpatterns = [
    path('documents/', ManageDocumentsView.as_view(), name='manage_documents'),
    path('documents/add/', AddDocumentView.as_view(), name='add_document'),
    path('documents/<int:pk>/edit/', EditDocumentView.as_view(), name='edit_document'),
    path('documents/<int:pk>/delete/', DeleteDocumentView.as_view(), name='delete_document'),
    path('placements/', ManagePlacementsView.as_view(), name='manage_placements'),
    path('placements/add/', AddPlacementView.as_view(), name='add_placement'),
    path('placements/<int:pk>/edit/', EditPlacementView.as_view(), name='edit_placement'),
    path('placements/<int:pk>/delete/', DeletePlacementView.as_view(), name='delete_placement'),
    path('labs/', ManageLabsView.as_view(), name='manage_labs'),
    path('labs/add/', AddLabView.as_view(), name='add_lab'),
    path('labs/<int:pk>/edit/', EditLabView.as_view(), name='edit_lab'),
    path('labs/<int:pk>/delete/', DeleteLabView.as_view(), name='delete_lab'),
]
