from django.urls import path, include
from elder import views
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register("profile", views.UserProfileViewset)
router.register("medstaff", views.MedicalStaffViewset)
router.register("patient", views.PatientRelativeViewset)
router.register("notification", views.NotificationViewset)

urlpatterns = [
    path("verify/", views.VerifyView.as_view()),
    path("email/", views.EmailView.as_view()),
    path("getHosp/<str:pk>", views.GetHospitalDetails.as_view()),
    path("getHospid/<str:pk>", views.GetHospID.as_view()),
    path("checkhospID/<str:pk>", views.CheckHospID.as_view()),
    path("getMessages/<str:pk>", views.GetMessages.as_view()),
    path("getnotid/<str:pk>", views.GetNotificationID.as_view()),
    path("getnotpat/<str:pk>", views.GetNotifiedPatient.as_view()),
    path("vitals/<str:pk>", views.VitalPatientDataView.as_view(), name="vital_list"),
    path("vitaldata/", views.Vitals.as_view(), name="vital_post"),
    path(
        "graph-dashboard/<str:pk>",
        views.VitalGraphDataView.as_view(),
        name="vital_graph",
    ),
    path("report-data/", views.ReportDataView.as_view(), name="report_data_post"),
    path(
        "report-data/<str:pk>", views.ReportDataView.as_view(), name="report_data_get"
    ),
    path("chart-data/<str:pk>", views.ChartDataView.as_view(), name="chart_data"),
    path(
        "relative-list/<str:pk>",
        views.PatientListViewRelative.as_view(),
        name="relative_list",
    ),
    path("relpat_data/", views.RelativePatientDataView.as_view(), name="relpat_view"),
    path("auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path(
        "auth/logout/blacklist/",
        views.BlacklistTokenUpdateView.as_view(),
        name="blacklist",
    ),
    path("imagepost/", views.ImageViewset.as_view(), name="posts_list"),
    path("hardwarepost/", views.CompareImages.as_view(), name="compare_images"),

    path("start-enroll/<str:model_id>/<int:patient_id>/", views.StartEnrollView.as_view(), name="start_enroll"),
    path("poll/<str:model_id>/", views.PollView.as_view(), name="poll"),
    path("poll/result/<str:model_id>/", views.PollResultView.as_view(), name="poll_result"),
    path("status/<str:model_id>/", views.StatusView.as_view(), name="status"),

    # path('falldetect/', views.Falldetection.as_view(), name="detect-fall"),
    path("", include(router.urls)),
]
