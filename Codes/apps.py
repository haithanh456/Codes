cat > extra/Codes/Codes/apps.py << 'EOF'
from django.apps import AppConfig

class CodesConfig(AppConfig):
    name = "Codes"
    dpy_package = "Codes"
EOF
