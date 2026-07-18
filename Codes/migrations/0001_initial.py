from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('bd_models', '0001_initial'),   
    ]

    operations = [
        migrations.CreateModel(
            name='RedeemCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50, unique=True)),
                ('reward_type', models.CharField(max_length=20, choices=[('ball', 'Countryball'), ('ball_special', 'Countryball + Special'), ('currency', 'Currency (Coins)')], default='ball')),
                ('ball', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bd_models.Ball')),
                ('special', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='bd_models.Special')),
                ('currency_amount', models.PositiveIntegerField(default=0)),
                ('expires_at', models.DateTimeField(blank=True, null=True)),
                ('max_uses', models.PositiveIntegerField(default=1)),
                ('current_uses', models.PositiveIntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
    ]
